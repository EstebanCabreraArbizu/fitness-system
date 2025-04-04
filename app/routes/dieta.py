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
        
        if isinstance(current_user, Client):
            # Si es cliente, ver sus dietas
            cursor.execute("""
                SELECT d.*, i.nombres as instructor_nombre, i.apellidos as instructor_apellidos,
                       disc.nombre as discipline_nombre
                FROM Dieta d
                JOIN Instructor i ON d.Instructor_id = i.id
                JOIN Discipline disc ON d.Discipline_id = disc.id
                WHERE d.Cliente_id = %s
                ORDER BY d.fecha_registro DESC
            """, (current_user.id,))
        elif isinstance(current_user, Instructor):
            # Si es instructor, ver las dietas que ha creado
            cursor.execute("""
                SELECT d.*, c.nombres as cliente_nombre, c.apellidos as cliente_apellidos,
                       disc.nombre as discipline_nombre
                FROM Dieta d
                JOIN Cliente c ON d.Cliente_id = c.id
                JOIN Discipline disc ON d.Discipline_id = disc.id
                WHERE d.Instructor_id = %s
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
    if not isinstance(current_user, Instructor):
        flash('Solo los instructores pueden crear dietas', 'warning')
        return redirect(url_for('dieta.index'))
        
    if request.method == 'GET':
        try:
            conn = get_db(current_app)
            cursor = conn.cursor()
            
            # Obtener clientes asignados al instructor
            cursor.execute("""
                SELECT c.*
                FROM Cliente c
                JOIN Cliente_Instructor ci ON c.id = ci.Cliente_id
                WHERE ci.Instructor_id = %s AND c.status = 1
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
            
            return render_template('dietas/nueva.html', clientes=clientes, disciplinas=disciplinas)
            
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
                Cliente_id, Instructor_id, Discipline_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            tipo_dieta, nombre, descripcion, fecha_inicio, fecha_fin, 
            duracion_dieta, edad, alergias, enfermedad_cronica, 
            alergia_medicamento, dias_semana, meta_calorias, 1,
            cliente_id, current_user.id, discipline_id
        ))
        
        dieta_id = cursor.lastrowid
        
        # Procesar imágenes de la dieta si existen
        if 'imagenes' in request.files:
            imagenes = request.files.getlist('imagenes')
            for imagen in imagenes:
                if imagen and imagen.filename:
                    filename = secure_filename(imagen.filename)
                    name_parts = os.path.splitext(filename)
                    unique_filename = f"dieta_{dieta_id}_{name_parts[0]}_{int(time.time())}{name_parts[1]}"
                    
                    # Guardar imagen
                    imagen_path = os.path.join('app/static/img/dietas', unique_filename)
                    imagen.save(imagen_path)
                    
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
            JOIN Cliente c ON d.Cliente_id = c.id
            JOIN Instructor i ON d.Instructor_id = i.id
            JOIN Discipline disc ON d.Discipline_id = disc.id
            WHERE d.id = %s
        """, (dieta_id,))
        
        dieta = cursor.fetchone()
        
        if not dieta:
            flash('Dieta no encontrada', 'warning')
            return redirect(url_for('dieta.index'))
        
        # Verificar permisos (solo el instructor que la creó o el cliente asignado pueden verla)
        if not (
            (isinstance(current_user, Instructor) and current_user.id == dieta['Instructor_id']) or
            (isinstance(current_user, Client) and current_user.id == dieta['Cliente_id'])
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
            'dietas/detalle.html', 
            dieta=dieta, 
            comidas=comidas,
            imagenes=imagenes,
            es_instructor=isinstance(current_user, Instructor)
        )
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar detalles de dieta: {str(e)}")
        flash('Error al cargar detalles de la dieta', 'danger')
        return redirect(url_for('dieta.index'))

@dieta.route('/<int:dieta_id>/agregar_comida', methods=['GET', 'POST'])
@login_required
def agregar_comida(dieta_id):
    """Agregar comida a una dieta"""
    if not isinstance(current_user, Instructor):
        flash('Solo los instructores pueden agregar comidas', 'warning')
        return redirect(url_for('dieta.detalle', dieta_id=dieta_id))
    
    # Verificar que la dieta pertenece al instructor
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM Dieta WHERE id = %s AND Instructor_id = %s",
            (dieta_id, current_user.id)
        )
        dieta = cursor.fetchone()
        cursor.close()
        
        if not dieta:
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
        if 'imagen' in request.files and request.files['imagen'].filename:
            imagen = request.files['imagen']
            filename = secure_filename(imagen.filename)
            name_parts = os.path.splitext(filename)
            unique_filename = f"comida_{name_parts[0]}_{int(time.time())}{name_parts[1]}"
            
            # Guardar imagen
            imagen_path = os.path.join('app/static/img/comidas', unique_filename)
            imagen.save(imagen_path)
            image_name = unique_filename
        
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