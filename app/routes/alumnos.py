from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.user import User
import os
import time
from datetime import date

alumnos = Blueprint('alumnos', __name__, template_folder='app/templates')

@alumnos.route('/', methods=['GET'])
@login_required
def index():
    """Lista los alumnos asignados a un instructor"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden acceder a esta sección', 'warning')
        return redirect(url_for('dieta.index'))
        
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener alumnos asignados al instructor actual
        cursor.execute("""
            SELECT u.*, 
                   cd.nivel_actividad, cd.direccion, cd.tipo_cliente,
                   IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as peso,
                   IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as altura,
                   (SELECT COUNT(*) FROM Rutina WHERE Usuario_id = u.id) as num_rutinas,
                   (SELECT COUNT(*) FROM Meta WHERE Usuario_id = u.id) as num_metas,
                   (SELECT COUNT(*) FROM Dieta WHERE Usuario_id = u.id AND Usuario_2_id = %s) as num_dietas,
                   IFNULL((
                       SELECT ROUND(AVG(calificacion_instructor) * 10)
                       FROM Seguimiento_Progreso 
                       WHERE Usuario_id = u.id 
                       ORDER BY fecha_seguimiento DESC 
                       LIMIT 5
                   ), 0) as seguimientos
            FROM Usuario u
            JOIN Cliente_datos cd ON u.id = cd.Usuario_id
            JOIN Cliente_Instructor ci ON u.id = ci.Usuario_id
            WHERE ci.Usuario_2_id = %s AND u.status = 1 AND u.Tipo_usuario_id = 1
            ORDER BY u.nombres
        """, (current_user.id, current_user.id))
        
        alumnos = cursor.fetchall()
        cursor.close()
        
        return render_template('alumnos/index.html', alumnos=alumnos)
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar alumnos: {str(e)}")
        flash(f'Error al cargar alumnos: {str(e)}', 'danger')
        return redirect(url_for('users.profile', user_id=current_user.id))

@alumnos.route('/asignar', methods=['GET', 'POST'])
@login_required
def asignar_alumno():
    """Asigna un alumno existente a un instructor"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden asignar alumnos', 'warning')
        return redirect(url_for('alumnos.index'))
    
    if request.method == 'GET':
        try:
            conn = get_db(current_app)
            cursor = conn.cursor()
            
            # Obtener todos los clientes que no están asignados a este instructor
            cursor.execute("""
                SELECT u.*, cd.nivel_actividad
                FROM Usuario u
                JOIN Cliente_datos cd ON u.id = cd.Usuario_id
                WHERE u.Tipo_usuario_id = 1 AND u.status = 1
                AND u.id NOT IN (
                    SELECT ci.Usuario_id 
                    FROM Cliente_Instructor ci 
                    WHERE ci.Usuario_2_id = %s
                )
            """, (current_user.id,))
            
            clientes_disponibles = cursor.fetchall()
            
            # Obtener disciplinas del instructor
            cursor.execute("""
                SELECT d.*
                FROM Discipline d
                JOIN Discipline_Instructor di ON d.id = di.Discipline_id
                WHERE di.Usuario_id = %s
            """, (current_user.id,))
            
            disciplinas = cursor.fetchall()
            
            cursor.close()
            
            return render_template('alumnos/asignar.html', 
                                 clientes=clientes_disponibles, 
                                 disciplinas=disciplinas)
            
        except Exception as e:
            current_app.logger.error(f"Error al preparar asignación: {str(e)}")
            flash(f'Error al cargar datos para asignación: {str(e)}', 'danger')
            return redirect(url_for('alumnos.index'))
    
    # Procesar POST para asignar alumno
    try:
        cliente_id = request.form.get('cliente_id')
        
        if not cliente_id:
            flash('Debes seleccionar un cliente para asignar', 'warning')
            return redirect(url_for('alumnos.asignar_alumno'))
        
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verificar que el cliente no esté ya asignado
        cursor.execute("""
            SELECT id FROM Cliente_Instructor 
            WHERE Usuario_id = %s AND Usuario_2_id = %s
        """, (cliente_id, current_user.id))
        
        if cursor.fetchone():
            flash('Este cliente ya está asignado a tu perfil', 'warning')
            return redirect(url_for('alumnos.index'))
        
        # Asignar cliente al instructor
        cursor.execute("""
            INSERT INTO Cliente_Instructor (Usuario_id, Usuario_2_id)
            VALUES (%s, %s)
        """, (cliente_id, current_user.id))
        
        conn.commit()
        cursor.close()
        
        flash('Cliente asignado exitosamente', 'success')
        return redirect(url_for('alumnos.index'))
        
    except Exception as e:
        current_app.logger.error(f"Error al asignar cliente: {str(e)}")
        flash(f'Error al asignar cliente: {str(e)}', 'danger')
        return redirect(url_for('alumnos.asignar_alumno'))

@alumnos.route('/detalles/<int:alumno_id>', methods=['GET'])
@login_required
def detalles_alumno(alumno_id):
    """Muestra los detalles de un alumno específico"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden ver detalles de alumnos', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verificar que el alumno está asignado al instructor
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        if not cursor.fetchone():
            flash('Este alumno no está asignado a tu perfil', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Obtener datos del alumno
        cursor.execute("""
            SELECT u.*, 
                   cd.nivel_actividad, cd.direccion, cd.tipo_cliente,
                   IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as peso,
                   IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as altura,
                   IFNULL((SELECT imc FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as imc
            FROM Usuario u
            JOIN Cliente_datos cd ON u.id = cd.Usuario_id
            WHERE u.id = %s
        """, (alumno_id,))
        
        alumno = cursor.fetchone()
        
        if not alumno:
            flash('Alumno no encontrado', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Obtener historial de medidas
        cursor.execute("""
            SELECT * FROM Historial_Medidas
            WHERE Usuario_id = %s
            ORDER BY fecha_medicion DESC
        """, (alumno_id,))
        
        medidas = cursor.fetchall()
        
        # Obtener rutinas asignadas
        cursor.execute("""
            SELECT r.*, 
                   (SELECT COUNT(*) FROM Ejercicio_Rutina er WHERE er.Rutina_id = r.id) as num_ejercicios
            FROM Rutina r
            WHERE r.Usuario_id = %s
            ORDER BY r.fecha_creacion DESC
        """, (alumno_id,))
        
        rutinas = cursor.fetchall()
        
        # Obtener metas asignadas
        cursor.execute("""
            SELECT * FROM Meta
            WHERE Usuario_id = %s
            ORDER BY fecha_inicio DESC
        """, (alumno_id,))
        
        metas = cursor.fetchall()
        
        # Obtener dietas asignadas
        cursor.execute("""
            SELECT d.*,
                   disc.nombre as discipline_nombre
            FROM Dieta d
            JOIN Discipline disc ON d.Discipline_id = disc.id
            WHERE d.Usuario_id = %s AND d.Usuario_2_id = %s
            ORDER BY d.fecha_registro DESC
        """, (alumno_id, current_user.id))
        
        dietas = cursor.fetchall()
        
        # Obtener seguimientos de progreso
        cursor.execute("""
            SELECT sp.*, 
                   r.nombre as rutina_nombre,
                   m.descripcion as meta_descripcion,
                   d.nombre as dieta_nombre
            FROM Seguimiento_Progreso sp
            LEFT JOIN Rutina r ON sp.Rutina_id = r.id
            LEFT JOIN Meta m ON sp.Meta_id = m.id
            LEFT JOIN Dieta d ON sp.Dieta_id = d.id
            WHERE sp.Usuario_id = %s
            ORDER BY sp.fecha_seguimiento DESC
        """, (alumno_id,))
        
        seguimientos = cursor.fetchall()
        
        cursor.close()
        
        return render_template('alumnos/detalles.html', 
                             alumno=alumno,
                             medidas=medidas,
                             rutinas=rutinas,
                             metas=metas,
                             dietas=dietas,
                             seguimientos=seguimientos)
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar detalles del alumno: {str(e)}")
        flash(f'Error al cargar detalles del alumno: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@alumnos.route('/eliminar/<int:alumno_id>', methods=['POST'])
@login_required
def eliminar_alumno(alumno_id):
    """Elimina la asignación entre un alumno y el instructor"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden eliminar alumnos', 'warning')
        return redirect(url_for('alumnos.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Eliminar la relación en Cliente_Instructor
        cursor.execute("""
            DELETE FROM Cliente_Instructor
            WHERE Usuario_id = %s AND Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        conn.commit()
        cursor.close()
        
        flash('Alumno eliminado de tu lista correctamente', 'success')
        return redirect(url_for('alumnos.index'))
        
    except Exception as e:
        current_app.logger.error(f"Error al eliminar alumno: {str(e)}")
        flash(f'Error al eliminar alumno: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@alumnos.route('/agregar_medida/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def agregar_medida(alumno_id):
    """Agrega una nueva medida para un alumno"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden agregar medidas', 'warning')
        return redirect(url_for('alumnos.index'))
    
    try:
        # Verificar que el alumno está asignado al instructor
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        if not cursor.fetchone():
            flash('Este alumno no está asignado a tu perfil', 'danger')
            return redirect(url_for('alumnos.index'))
        
        if request.method == 'GET':
            # Obtener datos del alumno
            cursor.execute("""
                SELECT u.nombres, u.apellidos
                FROM Usuario u
                WHERE u.id = %s
            """, (alumno_id,))
            
            alumno = cursor.fetchone()
            cursor.close()
            
            if not alumno:
                flash('Alumno no encontrado', 'danger')
                return redirect(url_for('alumnos.index'))
            
            return render_template('alumnos/agregar_medida.html', alumno_id=alumno_id, alumno=alumno)
        
        # Procesar POST para agregar medida
        peso = float(request.form.get('peso', 0))
        altura = float(request.form.get('altura', 0))
        
        if peso <= 0 or altura <= 0:
            flash('Los valores de peso y altura deben ser mayores a cero', 'warning')
            return redirect(url_for('alumnos.agregar_medida', alumno_id=alumno_id))
        
        # Calcular IMC
        imc = round(peso / ((altura / 100) ** 2), 2)
        
        # Guardar medida
        cursor.execute("""
            INSERT INTO Historial_Medidas (peso, altura, imc, Usuario_id)
            VALUES (%s, %s, %s, %s)
        """, (peso, altura, imc, alumno_id))
        
        conn.commit()
        cursor.close()
        
        flash('Medida agregada correctamente', 'success')
        return redirect(url_for('alumnos.detalles_alumno', alumno_id=alumno_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al agregar medida: {str(e)}")
        flash(f'Error al agregar medida: {str(e)}', 'danger')
        return redirect(url_for('alumnos.detalles_alumno', alumno_id=alumno_id))

@alumnos.route('/nuevo_seguimiento/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def nuevo_seguimiento(alumno_id):
    """Crea un nuevo seguimiento de progreso para un alumno"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden crear seguimientos', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verificar que el alumno está asignado al instructor
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        if not cursor.fetchone():
            flash('Este alumno no está asignado a tu perfil', 'danger')
            return redirect(url_for('alumnos.index'))
        
        if request.method == 'GET':
            # Obtener datos del alumno
            cursor.execute("""
                SELECT u.nombres, u.apellidos,
                       IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as peso,
                       IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as altura,
                       IFNULL((SELECT imc FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), 0) as imc
                FROM Usuario u
                WHERE u.id = %s
            """, (alumno_id,))
            
            alumno = cursor.fetchone()
            
            # Obtener rutinas activas del alumno
            cursor.execute("""
                SELECT r.id, r.nombre 
                FROM Rutina r
                WHERE r.Usuario_id = %s
                ORDER BY r.fecha_creacion DESC
            """, (alumno_id,))
            
            rutinas = cursor.fetchall()
            
            # Obtener metas activas del alumno
            cursor.execute("""
                SELECT m.id, m.descripcion
                FROM Meta m
                WHERE m.Usuario_id = %s AND m.estado = 'En progreso'
                ORDER BY m.fecha_inicio DESC
            """, (alumno_id,))
            
            metas = cursor.fetchall()
            
            # Obtener dietas activas del alumno
            cursor.execute("""
                SELECT d.id, d.nombre
                FROM Dieta d
                WHERE d.Usuario_id = %s AND d.Usuario_2_id = %s AND d.status = 1
                ORDER BY d.fecha_registro DESC
            """, (alumno_id, current_user.id))
            
            dietas = cursor.fetchall()
            
            cursor.close()
            
            if not alumno:
                flash('Alumno no encontrado', 'danger')
                return redirect(url_for('alumnos.index'))
            
            # Obtener la fecha actual para el formulario
            today = date.today().strftime('%Y-%m-%d')
            
            return render_template('alumnos/nuevo_seguimiento.html', 
                                 alumno=alumno,
                                 alumno_id=alumno_id,
                                 rutinas=rutinas,
                                 metas=metas,
                                 dietas=dietas,
                                 today=today)
        
        # Procesar POST para crear seguimiento
        # Obtener datos del formulario
        fecha_seguimiento = request.form.get('fecha_seguimiento')
        rutina_id = request.form.get('rutina_id') or None
        meta_id = request.form.get('meta_id') or None
        dieta_id = request.form.get('dieta_id') or None
        
        # Datos de peso y mediciones
        peso_actual = request.form.get('peso_actual') or None
        imc_actual = request.form.get('imc_actual') or None
        
        # Datos de rutina
        nivel_esfuerzo = request.form.get('nivel_esfuerzo') or None
        rendimiento = request.form.get('rendimiento') or None
        ejercicios_completados = request.form.get('ejercicios_completados') or None
        
        # Datos de dieta
        adherencia_dieta = request.form.get('adherencia_dieta') or None
        sensacion_hambre = request.form.get('sensacion_hambre') or None
        energia_diaria = request.form.get('energia_diaria') or None
        
        # Datos generales
        dificultades = request.form.get('dificultades') or None
        logros = request.form.get('logros') or None
        observaciones = request.form.get('observaciones') or None
        calificacion_instructor = request.form.get('calificacion_instructor') or None
        
        # Validaciones básicas
        if not fecha_seguimiento:
            flash('La fecha de seguimiento es obligatoria', 'warning')
            return redirect(url_for('alumnos.nuevo_seguimiento', alumno_id=alumno_id))
        
        # Crear seguimiento en la base de datos
        cursor.execute("""
            INSERT INTO Seguimiento_Progreso (
                Usuario_id, fecha_seguimiento, Rutina_id, Meta_id, Dieta_id,
                peso_actual, imc_actual, nivel_esfuerzo, rendimiento, ejercicios_completados,
                adherencia_dieta, sensacion_hambre, energia_diaria, dificultades, logros,
                observaciones, calificacion_instructor, instructor_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """, (
            alumno_id, fecha_seguimiento, rutina_id, meta_id, dieta_id,
            peso_actual, imc_actual, nivel_esfuerzo, rendimiento, ejercicios_completados,
            adherencia_dieta, sensacion_hambre, energia_diaria, dificultades, logros,
            observaciones, calificacion_instructor, current_user.id
        ))
        
        seguimiento_id = cursor.lastrowid
        
        # Procesar imágenes si existen
        if 'imagenes' in request.files:
            files = request.files.getlist('imagenes')
            for file in files:
                if file and file.filename.strip():
                    filename = secure_filename(file.filename)
                    # Generar nombre único con timestamp
                    name, ext = os.path.splitext(filename)
                    unique_filename = f"{name}_{int(time.time())}{ext}"
                    
                    # Guardar archivo
                    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'seguimiento', unique_filename)
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    file.save(file_path)
                    
                    tipo_imagen = request.form.get('tipo_imagen', 'progreso')
                    
                    # Registrar en base de datos
                    cursor.execute(
                        "INSERT INTO Seguimiento_Imagen (Seguimiento_Progreso_id, nombre_imagen, tipo) VALUES (%s, %s, %s)",
                        (seguimiento_id, unique_filename, tipo_imagen)
                    )
        
        # Si se ingresó un nuevo peso, también agregarlo al historial de medidas
        if peso_actual and float(peso_actual) > 0:
            # Obtener altura actual del alumno
            cursor.execute("""
                SELECT altura FROM Historial_Medidas 
                WHERE Usuario_id = %s 
                ORDER BY fecha_medicion DESC LIMIT 1
            """, (alumno_id,))
            
            altura_result = cursor.fetchone()
            altura = altura_result['altura'] if altura_result else 0
            
            if altura > 0:
                # Calcular IMC
                imc = round(float(peso_actual) / ((altura / 100) ** 2), 2)
                
                # Guardar nueva medida
                cursor.execute("""
                    INSERT INTO Historial_Medidas (peso, altura, imc, Usuario_id)
                    VALUES (%s, %s, %s, %s)
                """, (peso_actual, altura, imc, alumno_id))
        
        conn.commit()
        cursor.close()
        
        flash('Seguimiento registrado correctamente', 'success')
        return redirect(url_for('alumnos.detalles_alumno', alumno_id=alumno_id))
        
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Error al crear seguimiento: {str(e)}")
        flash(f'Error al crear seguimiento: {str(e)}', 'danger')
        return redirect(url_for('alumnos.nuevo_seguimiento', alumno_id=alumno_id))

@alumnos.route('/seguimiento/<int:seguimiento_id>', methods=['GET'])
@login_required
def detalle_seguimiento(seguimiento_id):
    """Muestra el detalle de un seguimiento específico"""
    if not current_user.is_authenticated:
        flash('Debes iniciar sesión para ver los detalles', 'warning')
        return redirect(url_for('users.login'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener detalles del seguimiento
        cursor.execute("""
            SELECT sp.*, 
                   u.nombres as alumno_nombre, u.apellidos as alumno_apellido,
                   i.nombres as instructor_nombre, i.apellidos as instructor_apellido,
                   r.nombre as rutina_nombre,
                   m.descripcion as meta_descripcion,
                   d.nombre as dieta_nombre
            FROM Seguimiento_Progreso sp
            JOIN Usuario u ON sp.Usuario_id = u.id
            JOIN Usuario i ON sp.instructor_id = i.id
            LEFT JOIN Rutina r ON sp.Rutina_id = r.id
            LEFT JOIN Meta m ON sp.Meta_id = m.id
            LEFT JOIN Dieta d ON sp.Dieta_id = d.id
            WHERE sp.id = %s
        """, (seguimiento_id,))
        
        seguimiento = cursor.fetchone()
        
        if not seguimiento:
            flash('Seguimiento no encontrado', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Verificar permisos
        alumno_id = seguimiento['Usuario_id']
        instructor_id = seguimiento['instructor_id']
        
        if current_user.is_instructor():
            # Verificar que el instructor está asignado al alumno
            cursor.execute("""
                SELECT ci.id 
                FROM Cliente_Instructor ci 
                WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
            """, (alumno_id, current_user.id))
            
            if not cursor.fetchone() and current_user.id != instructor_id:
                flash('No tienes permiso para ver este seguimiento', 'danger')
                return redirect(url_for('alumnos.index'))
        elif current_user.id != alumno_id:
            flash('No tienes permiso para ver este seguimiento', 'danger')
            return redirect(url_for('dieta.index'))
        
        # Obtener imágenes del seguimiento
        cursor.execute("""
            SELECT * FROM Seguimiento_Imagen
            WHERE Seguimiento_Progreso_id = %s
        """, (seguimiento_id,))
        
        imagenes = cursor.fetchall()
        
        cursor.close()
        
        return render_template('alumnos/detalle_seguimiento.html', 
                             seguimiento=seguimiento,
                             imagenes=imagenes)
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar detalle de seguimiento: {str(e)}")
        flash(f'Error al cargar detalle del seguimiento: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index')) 