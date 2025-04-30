import os
import time
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.servicio import Servicio
from app.models.user import User

servicios = Blueprint('servicios', __name__, template_folder='app/templates')

# Asegurar que existan las tablas necesarias
@servicios.before_app_request
def crear_tablas():
    Servicio.crear_tablas_si_no_existen()

# Funciones auxiliares
def process_service_image(request):
    """Procesa la imagen del servicio"""
    imagen_file = request.files.get('imagen')
    
    if not imagen_file or not imagen_file.filename:
        return 'default-service.png'
    
    filename = secure_filename(imagen_file.filename)
    
    # Añadir timestamp para evitar colisiones
    name_parts = os.path.splitext(filename)
    unique_filename = f"service_{name_parts[0]}_{int(time.time())}{name_parts[1]}"
    
    # Verificar tipo de archivo
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' in unique_filename and unique_filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        img_path = os.path.join('app/static/img/servicios', unique_filename)
        
        # Asegurar que existe el directorio
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        imagen_file.save(img_path)
        
        # Optimizar imagen
        try:
            from PIL import Image
            img = Image.open(img_path)
            # Redimensionar si es demasiado grande
            if img.width > 800 or img.height > 800:
                img.thumbnail((800, 800), Image.LANCZOS)
            # Guardar con compresión
            img.save(img_path, optimize=True, quality=85)
        except ImportError:
            current_app.logger.warning("PIL no disponible, no se puede optimizar la imagen")
        
        return unique_filename
    else:
        return None, 'Formato de imagen no permitido. Use: png, jpg, jpeg, gif, webp'

@servicios.route('/instructor/servicios')
@login_required
def index():
    """Lista los servicios del instructor"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    servicios = Servicio.obtener_todos_por_instructor(current_user.id)
    
    return render_template('servicios/index.html', servicios=servicios)

@servicios.route('/instructor/servicios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo():
    """Crea un nuevo servicio"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    if request.method == 'GET':
        return render_template('servicios/nuevo.html')
    
    try:
        # Obtener datos del formulario
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', 0)
        duracion = request.form.get('duracion', 60)
        categoria = request.form.get('categoria', '').strip()
        modalidad = request.form.get('modalidad', '').strip()
        nivel = request.form.get('nivel', '').strip()
        
        # Validar datos
        if not nombre or not descripcion or not categoria or not modalidad or not nivel:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return render_template('servicios/nuevo.html')
        
        # Procesar precio como decimal
        try:
            precio = float(precio)
            if precio < 0:
                flash('El precio no puede ser negativo', 'warning')
                return render_template('servicios/nuevo.html')
        except ValueError:
            flash('El precio debe ser un número válido', 'warning')
            return render_template('servicios/nuevo.html')
        
        # Procesar duración como entero
        try:
            duracion = int(duracion)
            if duracion <= 0 or duracion > 60:
                flash('La duración debe estar entre 1 y 60 minutos', 'warning')
                return render_template('servicios/nuevo.html')
        except ValueError:
            flash('La duración debe ser un número entero válido', 'warning')
            return render_template('servicios/nuevo.html')
        
        # Procesar imagen
        imagen = process_service_image(request)
        if isinstance(imagen, tuple):
            flash(imagen[1], 'warning')
            return render_template('servicios/nuevo.html')
        
        # Crear servicio
        servicio_data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'duracion': duracion,
            'categoria': categoria,
            'modalidad': modalidad,
            'nivel': nivel,
            'imagen': imagen,
            'instructor_id': current_user.id
        }
        
        # Procesar horarios si se proporcionan
        horarios_data = []
        
        # En caso de enviar múltiples horarios por formulario
        dias_semana = request.form.getlist('dia_semana[]')
        horas_inicio = request.form.getlist('hora_inicio[]')
        horas_fin = request.form.getlist('hora_fin[]')
        cupos = request.form.getlist('cupos[]')
        
        if dias_semana and horas_inicio and horas_fin:
            for i in range(len(dias_semana)):
                if i < len(horas_inicio) and i < len(horas_fin):
                    cupo = 1
                    if i < len(cupos) and cupos[i]:
                        try:
                            cupo = int(cupos[i])
                            if cupo < 1:
                                cupo = 1
                        except ValueError:
                            cupo = 1
                    
                    horarios_data.append({
                        'dia_semana': dias_semana[i],
                        'hora_inicio': horas_inicio[i],
                        'hora_fin': horas_fin[i],
                        'cupos_disponibles': cupo
                    })
        
        servicio_id = Servicio.crear(servicio_data, horarios_data)
        
        if servicio_id:
            flash('Servicio creado exitosamente', 'success')
            return redirect(url_for('servicios.ver', servicio_id=servicio_id))
        else:
            flash('Error al crear el servicio. Intente de nuevo.', 'danger')
            return render_template('servicios/nuevo.html')
    
    except Exception as e:
        current_app.logger.error(f"Error al crear servicio: {str(e)}")
        flash(f'Error al crear servicio: {str(e)}', 'danger')
        return render_template('servicios/nuevo.html')

@servicios.route('/instructor/servicios/<int:servicio_id>')
@login_required
def ver(servicio_id):
    """Ver detalles de un servicio"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        current_app.logger.info(f"Solicitando servicio ID: {servicio_id} para instructor ID: {current_user.id}")
        servicio = Servicio.obtener_por_id(servicio_id, current_user.id)
        
        if not servicio:
            flash('Servicio no encontrado o no tiene permisos para acceder', 'warning')
            return redirect(url_for('servicios.index'))
        
        # Validar explícitamente que horarios esté presente
        if 'horarios' not in servicio:
            current_app.logger.warning(f"No se encontraron horarios para el servicio {servicio_id}")
            servicio['horarios'] = []
        
        current_app.logger.info(f"Servicio encontrado: {servicio['nombre']} con {len(servicio['horarios'])} horarios")
        
        # Ajustar formato de fecha-hora si es necesario
        for horario in servicio['horarios']:
            if not isinstance(horario['hora_inicio'], str):
                current_app.logger.debug(f"Formateando hora: {horario['hora_inicio']}")
        
        # Incluir fecha actual para el formulario de reserva
        from datetime import datetime
        now = datetime.now()
        
        return render_template('servicios/ver.html', servicio=servicio, now=now)
    except Exception as e:
        current_app.logger.error(f"Error al obtener detalles del servicio: {str(e)}")
        flash(f'Error al cargar el servicio: {str(e)}', 'danger')
        return redirect(url_for('servicios.index'))

@servicios.route('/instructor/servicios/<int:servicio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar(servicio_id):
    """Edita un servicio existente"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    servicio = Servicio.obtener_por_id(servicio_id, current_user.id)
    
    if not servicio:
        flash('Servicio no encontrado o no tiene permisos para acceder', 'warning')
        return redirect(url_for('servicios.index'))
    
    if request.method == 'GET':
        return render_template('servicios/editar.html', servicio=servicio)
    
    try:
        # Obtener datos del formulario
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        precio = request.form.get('precio', 0)
        duracion = request.form.get('duracion', 60)
        categoria = request.form.get('categoria', '').strip()
        modalidad = request.form.get('modalidad', '').strip()
        nivel = request.form.get('nivel', '').strip()
        estado = request.form.get('estado', 'activo')
        
        # Validar datos
        if not nombre or not descripcion or not categoria or not modalidad or not nivel:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return render_template('servicios/editar.html', servicio=servicio)
        
        # Procesar precio como decimal
        try:
            precio = float(precio)
            if precio < 0:
                flash('El precio no puede ser negativo', 'warning')
                return render_template('servicios/editar.html', servicio=servicio)
        except ValueError:
            flash('El precio debe ser un número válido', 'warning')
            return render_template('servicios/editar.html', servicio=servicio)
        
        # Procesar duración como entero
        try:
            duracion = int(duracion)
            if duracion <= 0 or duracion > 60:
                flash('La duración debe estar entre 1 y 60 minutos', 'warning')
                return render_template('servicios/editar.html', servicio=servicio)
        except ValueError:
            flash('La duración debe ser un número entero válido', 'warning')
            return render_template('servicios/editar.html', servicio=servicio)
        
        # Procesar imagen si se proporciona
        servicio_data = {
            'nombre': nombre,
            'descripcion': descripcion,
            'precio': precio,
            'duracion': duracion,
            'categoria': categoria,
            'modalidad': modalidad,
            'nivel': nivel,
            'estado': estado
        }
        
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename:
            imagen = process_service_image(request)
            if isinstance(imagen, tuple):
                flash(imagen[1], 'warning')
                return render_template('servicios/editar.html', servicio=servicio)
            servicio_data['imagen'] = imagen
        
        # Actualizar servicio
        actualizado = Servicio.actualizar(servicio_id, servicio_data, current_user.id)
        
        if actualizado:
            flash('Servicio actualizado exitosamente', 'success')
            return redirect(url_for('servicios.ver', servicio_id=servicio_id))
        else:
            flash('Error al actualizar el servicio. Intente de nuevo.', 'danger')
            return render_template('servicios/editar.html', servicio=servicio)
    
    except Exception as e:
        current_app.logger.error(f"Error al actualizar servicio: {str(e)}")
        flash(f'Error al actualizar servicio: {str(e)}', 'danger')
        return render_template('servicios/editar.html', servicio=servicio)

@servicios.route('/instructor/servicios/<int:servicio_id>/eliminar', methods=['POST'])
@login_required
def eliminar(servicio_id):
    """Elimina un servicio"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    eliminado = Servicio.eliminar(servicio_id, current_user.id)
    
    if eliminado:
        flash('Servicio eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el servicio', 'danger')
    
    return redirect(url_for('servicios.index'))

@servicios.route('/instructor/servicios/<int:servicio_id>/horarios', methods=['GET', 'POST'])
@login_required
def horarios(servicio_id):
    """Gestiona los horarios de un servicio"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    servicio = Servicio.obtener_por_id(servicio_id, current_user.id)
    
    if not servicio:
        flash('Servicio no encontrado o no tiene permisos para acceder', 'warning')
        return redirect(url_for('servicios.index'))
    
    if request.method == 'GET':
        return render_template('servicios/horarios.html', servicio=servicio)
    
    try:
        # Agregar nuevo horario
        dia_semana = request.form.get('dia_semana', '').strip()
        hora_inicio = request.form.get('hora_inicio', '').strip()
        hora_fin = request.form.get('hora_fin', '').strip()
        cupos = request.form.get('cupos', 1)
        
        # Validar datos
        if not dia_semana or not hora_inicio or not hora_fin:
            flash('Todos los campos son obligatorios', 'warning')
            return redirect(url_for('servicios.horarios', servicio_id=servicio_id))
        
        # Procesar cupos como entero
        try:
            cupos = int(cupos)
            if cupos < 1:
                cupos = 1
        except ValueError:
            cupos = 1
        
        # Crear horario
        horario_data = {
            'dia_semana': dia_semana,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'cupos_disponibles': cupos
        }
        
        horario_id = Servicio.agregar_horario(servicio_id, horario_data, current_user.id)
        
        if horario_id:
            flash('Horario agregado exitosamente', 'success')
        else:
            flash('Error al agregar horario. La duración debe ser menor a 60 minutos.', 'danger')
        
        return redirect(url_for('servicios.horarios', servicio_id=servicio_id))
    
    except Exception as e:
        current_app.logger.error(f"Error al agregar horario: {str(e)}")
        flash(f'Error al agregar horario: {str(e)}', 'danger')
        return redirect(url_for('servicios.horarios', servicio_id=servicio_id))

@servicios.route('/instructor/servicios/horario/<int:horario_id>/eliminar', methods=['POST'])
@login_required
def eliminar_horario(horario_id):
    """Elimina un horario de servicio"""
    if not current_user.is_instructor():
        flash('Esta sección es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    servicio_id = request.form.get('servicio_id')
    eliminado = Servicio.eliminar_horario(horario_id, current_user.id)
    
    if eliminado:
        flash('Horario eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar el horario', 'danger')
    
    return redirect(url_for('servicios.horarios', servicio_id=servicio_id))

# API para consultar servicios
@servicios.route('/api/servicios/<int:servicio_id>/horarios')
def api_horarios(servicio_id):
    """API para obtener horarios de un servicio"""
    horarios = Servicio.obtener_horarios_por_servicio(servicio_id)
    
    # Formatear para API
    horarios_formateados = []
    for h in horarios:
        horarios_formateados.append({
            'id': h['id'],
            'dia_semana': h['dia_semana'],
            'hora_inicio': h['hora_inicio'].strftime('%H:%M'),
            'hora_fin': h['hora_fin'].strftime('%H:%M'),
            'cupos_disponibles': h['cupos_disponibles']
        })
    
    return jsonify(horarios_formateados)

@servicios.route('/servicios/reservar', methods=['POST'])
@login_required
def reservar():
    """Reserva un servicio en un horario específico"""
    if current_user.is_instructor():
        flash('Los instructores no pueden reservar servicios', 'warning')
        return redirect(url_for('servicios.catalogo'))
    
    try:
        horario_id = request.form.get('horario_id')
        fecha = request.form.get('fecha')
        comentarios = request.form.get('comentarios', '')
        
        if not horario_id or not fecha:
            flash('El horario y la fecha son obligatorios', 'warning')
            return redirect(url_for('servicios.catalogo'))
        
        # Verificar que el horario exista y tenga cupos disponibles
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sh.*, s.nombre as servicio_nombre
            FROM Servicio_Horario sh
            JOIN Servicio s ON sh.servicio_id = s.id
            WHERE sh.id = %s AND sh.estado = 'activo' AND sh.cupos_disponibles > 0
        """, (horario_id,))
        
        horario = cursor.fetchone()
        
        if not horario:
            flash('El horario seleccionado no está disponible', 'warning')
            return redirect(url_for('servicios.catalogo'))
        
        # Verificar que no haya reservado el mismo horario en la misma fecha
        cursor.execute("""
            SELECT id FROM Servicio_Reserva
            WHERE horario_id = %s AND usuario_id = %s AND fecha = %s AND estado != 'cancelada'
        """, (horario_id, current_user.id, fecha))
        
        if cursor.fetchone():
            flash('Ya tienes una reserva para este horario en esta fecha', 'warning')
            return redirect(url_for('servicios.detalle', servicio_id=horario['servicio_id']))
        
        # Crear la reserva
        cursor.execute("""
            INSERT INTO Servicio_Reserva (horario_id, usuario_id, fecha, comentarios)
            VALUES (%s, %s, %s, %s)
        """, (horario_id, current_user.id, fecha, comentarios))
        
        # Actualizar cupos disponibles
        cursor.execute("""
            UPDATE Servicio_Horario 
            SET cupos_disponibles = cupos_disponibles - 1
            WHERE id = %s
        """, (horario_id,))
        
        conn.commit()
        cursor.close()
        
        flash(f'Reserva para {horario["servicio_nombre"]} realizada con éxito', 'success')
        return redirect(url_for('servicios.detalle', servicio_id=horario['servicio_id']))
        
    except Exception as e:
        current_app.logger.error(f"Error al reservar servicio: {str(e)}")
        flash(f'Error al realizar la reserva: {str(e)}', 'danger')
        return redirect(url_for('servicios.catalogo'))

# Rutas para catálogo de servicios (público)
@servicios.route('/servicios')
def catalogo():
    """Catálogo público de servicios"""
    conn = get_db(current_app)
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.*, 
                   u.nombres as instructor_nombre, 
                   u.apellidos as instructor_apellido,
                   u.imagen as instructor_imagen,
                   COUNT(DISTINCT sh.id) as total_horarios
            FROM Servicio s
            JOIN Usuario u ON s.instructor_id = u.id
            LEFT JOIN Servicio_Horario sh ON s.id = sh.servicio_id AND sh.estado = 'activo'
            WHERE s.estado = 'activo'
            GROUP BY s.id
            ORDER BY s.fecha_creacion DESC
        """)
        
        servicios = cursor.fetchall()
        return render_template('servicios/catalogo.html', servicios=servicios)
    except Exception as e:
        current_app.logger.error(f"Error al obtener catálogo de servicios: {str(e)}")
        flash('Error al cargar los servicios disponibles', 'danger')
        return render_template('servicios/catalogo.html', servicios=[])
    finally:
        cursor.close()

@servicios.route('/servicios/<int:servicio_id>')
def detalle(servicio_id):
    """Detalle público de un servicio"""
    try:
        current_app.logger.info(f"Solicitando detalle público de servicio ID: {servicio_id}")
        servicio = Servicio.obtener_por_id(servicio_id)
        
        if not servicio or servicio['estado'] != 'activo':
            flash('Servicio no encontrado', 'warning')
            return redirect(url_for('servicios.catalogo'))
        
        # Validar explícitamente que horarios esté presente
        if 'horarios' not in servicio:
            current_app.logger.warning(f"No se encontraron horarios para el servicio {servicio_id}")
            servicio['horarios'] = []
            
        current_app.logger.info(f"Servicio público encontrado: {servicio['nombre']} con {len(servicio['horarios'])} horarios")
        
        # Obtener información del instructor
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                SELECT u.id, u.nombres, u.apellidos, u.imagen, 
                       IFNULL((SELECT especialidad FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), '') as especialidad,
                       IFNULL((SELECT anios_experiencia FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), 0) as anios_experiencia
                FROM Usuario u
                WHERE u.id = %s
            """, (servicio['instructor_id'],))
            
            instructor = cursor.fetchone()
            
            # Incluir fecha actual para el formulario de reserva
            from datetime import datetime
            now = datetime.now()
            
            return render_template('servicios/detalle.html', servicio=servicio, instructor=instructor, now=now)
        except Exception as e:
            current_app.logger.error(f"Error al obtener información del instructor: {str(e)}")
            flash('Error al cargar los detalles del servicio', 'danger')
            return redirect(url_for('servicios.catalogo'))
        finally:
            cursor.close()
    except Exception as e:
        current_app.logger.error(f"Error al obtener detalle del servicio: {str(e)}")
        flash(f'Error al cargar el servicio: {str(e)}', 'danger')
        return redirect(url_for('servicios.catalogo')) 