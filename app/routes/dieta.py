from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.client import Client
from app.models.instructor import Instructor
import os
import time

dieta = Blueprint('dieta', __name__, template_folder='app/templates')

@dieta.route('/', methods=['GET'])
@login_required
def index():
    """Lista las dietas según el tipo de usuario"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        if current_user.is_client():
            # Si es cliente, ver sus dietas
            cursor.execute("""
                SELECT d.*, 
                       ins.nombres as instructor_nombre, 
                       ins.apellidos as instructor_apellidos,
                       disc.nombre as discipline_nombre
                FROM Dieta d
                JOIN Usuario ins ON d.Usuario_2_id = ins.id
                JOIN Discipline disc ON d.Discipline_id = disc.id
                WHERE d.Usuario_id = %s
                ORDER BY d.fecha_registro DESC
            """, (current_user.id,))
        elif current_user.is_instructor():
            # Si es instructor, ver las dietas que ha creado
            cursor.execute("""
                SELECT d.*, 
                       cli.nombres as cliente_nombre, 
                       cli.apellidos as cliente_apellidos,
                       disc.nombre as discipline_nombre
                FROM Dieta d
                JOIN Usuario cli ON d.Usuario_id = cli.id
                JOIN Discipline disc ON d.Discipline_id = disc.id
                WHERE d.Usuario_2_id = %s
                ORDER BY d.fecha_registro DESC
            """, (current_user.id,))
        else:
            flash('Tipo de usuario no reconocido', 'danger')
            return redirect(url_for('users.login'))
            
        dietas = cursor.fetchall()
        cursor.close()
        
        return render_template('dietas/index.html', dietas=dietas)
        
    except Exception as e:
        current_app.logger.error(f"Error al listar dietas: {str(e)}")
        flash('Error al cargar las dietas', 'danger')
        return render_template('dietas/index.html', dietas=[])
    
@dieta.route('/nueva', methods=['GET', 'POST'])
@login_required
def nueva_dieta():
    """Crear nueva dieta"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden crear dietas', 'warning')
        return redirect(url_for('dieta.index'))
        
    if request.method == 'GET':
        try:
            conn = get_db(current_app)
            cursor = conn.cursor()
            
            # Obtener clientes asignados al instructor
            cursor.execute("""
                SELECT u.*, 
                       cd.direccion, cd.tipo_cliente, cd.nivel_actividad, 
                       IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as peso,
                       IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as altura
                FROM Usuario u
                JOIN Cliente_datos cd ON u.id = cd.Usuario_id
                JOIN Cliente_Instructor ci ON u.id = ci.Usuario_id
                WHERE ci.Usuario_2_id = %s AND u.status = 1 AND u.Tipo_usuario_id = 1
            """, (current_user.id,))
            clientes = cursor.fetchall()
            
            # Obtener disciplinas del instructor
            cursor.execute("""
                SELECT d.*
                FROM Discipline d
                JOIN Discipline_Instructor di ON d.id = di.Discipline_id
                WHERE di.Instructor_id = %s
            """, (current_user.id,))
            disciplinas = cursor.fetchall()
            
            cursor.close()
            
            return render_template('dietas/crear-dieta.html', clientes=clientes, disciplinas=disciplinas)
            
        except Exception as e:
            current_app.logger.error(f"Error al preparar nueva dieta: {str(e)}")
            flash('Error al cargar información necesaria', 'danger')
            return redirect(url_for('dieta.index'))
    
    # Procesar POST para crear dieta
    try:
        # Extraer datos del formulario
        cliente_id = request.form.get('cliente_id')
        discipline_id = request.form.get('discipline_id')
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        tipo_dieta = request.form.get('tipo_dieta', '').strip()
        fecha_inicio = request.form.get('fecha_inicio')
        fecha_fin = request.form.get('fecha_fin')
        duracion_dieta = request.form.get('duracion_dieta', '').strip()
        edad = request.form.get('edad', '').strip()
        alergias = request.form.get('alergias', '').strip()
        enfermedad_cronica = request.form.get('enfermedad_cronica', '').strip()
        alergia_medicamento = request.form.get('alergia_medicamento', '').strip()
        dias_semana = request.form.get('dias_semana', '').strip()
        meta_calorias = request.form.get('meta_calorias', 0)
        
        # Validaciones básicas
        if not cliente_id or not discipline_id or not nombre or not fecha_inicio or not fecha_fin:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return redirect(url_for('dieta.nueva_dieta'))
        
        # Crear la dieta en la base de datos
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Dieta (
                tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, 
                duracion_dieta, edad, alergias, enfermedad_cronica, 
                alergia_medicamento, dias_semana, meta_calorias, status, 
                Discipline_id, Usuario_id, Usuario_2_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, 
            duracion_dieta, edad, alergias, enfermedad_cronica, 
            alergia_medicamento, dias_semana, meta_calorias, 1,
            discipline_id, cliente_id, current_user.id
        ))
        
        dieta_id = cursor.lastrowid
        
        # Procesar imágenes de la dieta si existen
        if 'imagenes' in request.files:
            files = request.files.getlist('imagenes')
            for file in files:
                if file and file.filename.strip():
                    filename = secure_filename(file.filename)
                    # Generar nombre único con timestamp
                    name, ext = os.path.splitext(filename)
                    unique_filename = f"{name}_{int(time.time())}{ext}"
                    
                    # Guardar archivo
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'dietas', unique_filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    
                    # Registrar en base de datos
                    cursor.execute(
                        "INSERT INTO Dieta_images (image_name, Dieta_id) VALUES (%s, %s)",
                        (unique_filename, dieta_id)
                    )
        
        conn.commit()
        cursor.close()
        
        flash(f'Dieta "{nombre}" creada exitosamente', 'success')
        return redirect(url_for('dieta.detalle', dieta_id=dieta_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al crear dieta: {str(e)}")
        flash(f'Error al crear dieta: {str(e)}', 'danger')
        return redirect(url_for('dieta.nueva_dieta'))

@dieta.route('/<int:dieta_id>', methods=['GET'])
@login_required
def detalle(dieta_id):
    """Ver detalles de una dieta"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la dieta
        cursor.execute("""
            SELECT d.*, 
                c.nombres as cliente_nombre, c.apellidos as cliente_apellidos,
                i.nombres as instructor_nombre, i.apellidos as instructor_apellidos,
                disc.nombre as discipline_nombre
            FROM Dieta d
            JOIN Usuario c ON d.Usuario_id = c.id
            JOIN Usuario i ON d.Usuario_2_id = i.id
            JOIN Discipline disc ON d.Discipline_id = disc.id
            WHERE d.id = %s
        """, (dieta_id,))
        
        dietas = cursor.fetchone()
        
        if not dietas:
            flash('Dieta no encontrada', 'warning')
            return redirect(url_for('dieta.index'))
        
        # Verificar permisos (solo el instructor que la creó o el cliente asignado pueden verla)
        if not (
            (current_user.is_instructor() and current_user.id == dietas['Usuario_2_id']) or
            (current_user.is_client() and current_user.id == dietas['Usuario_id'])
        ):
            flash('No tienes permiso para ver esta dieta', 'danger')
            return redirect(url_for('dieta.index'))
        
        # Obtener comidas de la dieta
        cursor.execute("""
            SELECT * FROM Comida 
            WHERE Dieta_id = %s
            ORDER BY dia_dieta, hora
        """, (dieta_id,))
        comidas = cursor.fetchall()
        
        # Obtener imágenes de la dieta
        cursor.execute("SELECT * FROM Dieta_images WHERE Dieta_id = %s", (dieta_id,))
        imagenes = cursor.fetchall()
        
        cursor.close()
        
        return render_template(
            'dietas/detalle_dieta.html', 
            dieta=dietas, 
            comidas=comidas,
            imagenes=imagenes,
            es_instructor=current_user.is_instructor()
        )
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar detalles de dieta: {str(e)}")
        flash('Error al cargar detalles de la dieta', 'danger')
        return redirect(url_for('dieta.index'))

@dieta.route('/<int:dieta_id>/agregar_comida', methods=['GET', 'POST'])
@login_required
def agregar_comida(dieta_id):
    """Agregar comida a una dieta"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden agregar comidas', 'warning')
        return redirect(url_for('dieta.detalle', dieta_id=dieta_id))
    
    # Verificar que la dieta pertenece al instructor
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Dieta WHERE id = %s AND Usuario_2_id = %s",
            (dieta_id, current_user.id)
        )
        dietas = cursor.fetchone()
        cursor.close()
        
        if not dietas:
            flash('No tienes permiso para modificar esta dieta', 'danger')
            return redirect(url_for('dieta.index'))
            
    except Exception as e:
        current_app.logger.error(f"Error al verificar permisos: {str(e)}")
        flash('Error al verificar permisos', 'danger')
        return redirect(url_for('dieta.index'))
    
    if request.method == 'GET':
        return render_template('dietas/agregar_comida.html', dieta_id=dieta_id)
    
    # Procesar POST para agregar comida
    try:
        # Extraer datos del formulario
        tipo_comida = request.form.get('tipo_comida', '').strip()
        dia_dieta = request.form.get('dia_dieta', '').strip()
        hora = request.form.get('hora', '').strip()
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        calorias = int(request.form.get('calorias', 0))
        proteinas = float(request.form.get('proteinas', 0))
        carbohidratos = float(request.form.get('carbohidratos', 0))
        grasas = float(request.form.get('grasas', 0))
        recomendacion = request.form.get('recomendacion', '').strip()
        
        # Validaciones básicas
        if not tipo_comida or not dia_dieta or not hora or not nombre:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return redirect(url_for('dieta.agregar_comida', dieta_id=dieta_id))
        
        # Procesar imagen de la comida si existe
        image_name = 'default-food.png'  # Imagen por defecto
        if 'imagenes' in request.files:
            files = request.files.getlist('imagenes')
            for file in files:
                if file and file.filename.strip():
                    filename = secure_filename(file.filename)
                    # Generar nombre único con timestamp
                    name, ext = os.path.splitext(filename)
                    unique_filename = f"{name}_{int(time.time())}{ext}"
                    
                    # Guardar archivo
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'dietas', unique_filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    
                    # Registrar en base de datos
                    cursor.execute(
                        "INSERT INTO Dieta_images (image_name, Dieta_id) VALUES (%s, %s)",
                        (unique_filename, dieta_id)
                    )
            
        # Crear la comida en la base de datos
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO Comida (
                tipo_comida, dia_dieta, hora, nombre, descripcion,
                calorias, proteinas, carbohidratos, grasas,
                recomendacion, image_name, status, Dieta_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            tipo_comida, dia_dieta, hora, nombre, descripcion,
            calorias, proteinas, carbohidratos, grasas,
            recomendacion, image_name, 1, dieta_id
        ))
        
        conn.commit()
        cursor.close()
        
        flash('Comida agregada exitosamente a la dieta', 'success')
        return redirect(url_for('dieta.detalle', dieta_id=dieta_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al agregar comida: {str(e)}")
        flash(f'Error al agregar comida: {str(e)}', 'danger')
        return redirect(url_for('dieta.agregar_comida', dieta_id=dieta_id))