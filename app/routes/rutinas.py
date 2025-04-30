from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.user import User
import os
import time
from datetime import datetime

rutinas = Blueprint('rutinas', __name__, template_folder='app/templates')

@rutinas.route('/<int:alumno_id>', methods=['GET'])
@login_required
def index(alumno_id):
    """Lista las rutinas de un alumno específico"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden acceder a esta sección', 'warning')
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
            SELECT u.nombres, u.apellidos
            FROM Usuario u
            WHERE u.id = %s
        """, (alumno_id,))
        
        alumno = cursor.fetchone()
        
        if not alumno:
            flash('Alumno no encontrado', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Obtener rutinas del alumno
        cursor.execute("""
            SELECT r.*, 
                   (SELECT COUNT(*) FROM Ejercicio_Rutina er WHERE er.Rutina_id = r.id) as num_ejercicios
            FROM Rutina r
            WHERE r.Usuario_id = %s
            ORDER BY r.fecha_creacion DESC
        """, (alumno_id,))
        
        rutinas = cursor.fetchall()
        
        # Obtener metas del alumno
        cursor.execute("""
            SELECT * FROM Meta
            WHERE Usuario_id = %s
            ORDER BY fecha_inicio DESC
        """, (alumno_id,))
        
        metas = cursor.fetchall()
        
        cursor.close()
        
        return render_template('rutinas/index.html', 
                             alumno=alumno,
                             alumno_id=alumno_id,
                             rutinas=rutinas,
                             metas=metas)
        
    except Exception as e:
        current_app.logger.error(f"Error al listar rutinas: {str(e)}")
        flash(f'Error al cargar rutinas: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@rutinas.route('/nueva/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def nueva_rutina(alumno_id):
    """Crea una nueva rutina para un alumno"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden crear rutinas', 'warning')
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
                SELECT u.nombres, u.apellidos
                FROM Usuario u
                WHERE u.id = %s
            """, (alumno_id,))
            
            alumno = cursor.fetchone()
            
            # Obtener ejercicios disponibles
            cursor.execute("""
                SELECT * FROM Ejercicio
                ORDER BY nombre
            """)
            
            ejercicios = cursor.fetchall()
            cursor.close()
            
            if not alumno:
                flash('Alumno no encontrado', 'danger')
                return redirect(url_for('alumnos.index'))
            
            return render_template('rutinas/nueva.html', 
                                 alumno=alumno,
                                 alumno_id=alumno_id,
                                 ejercicios=ejercicios)
        
        # Procesar POST para crear rutina
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        
        # Validaciones básicas
        if not nombre:
            flash('El nombre de la rutina es obligatorio', 'warning')
            return redirect(url_for('rutinas.nueva_rutina', alumno_id=alumno_id))
        
        # Crear rutina
        cursor.execute("""
            INSERT INTO Rutina (nombre, descripcion, Usuario_id)
            VALUES (%s, %s, %s)
        """, (nombre, descripcion, alumno_id))
        
        rutina_id = cursor.lastrowid
        
        # Procesar ejercicios seleccionados
        ejercicios = request.form.getlist('ejercicios[]')
        
        for i, ejercicio_id in enumerate(ejercicios, 1):
            cursor.execute("""
                INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id)
                VALUES (%s, %s, %s)
            """, (i, ejercicio_id, rutina_id))
        
        # Procesar meta asociada
        if 'crear_meta' in request.form and request.form.get('crear_meta') == '1':
            descripcion_meta = request.form.get('descripcion_meta', '').strip()
            fecha_inicio = request.form.get('fecha_inicio', '')
            fecha_fin = request.form.get('fecha_fin', '')
            estado = 'En progreso'
            
            if descripcion_meta and fecha_inicio and fecha_fin:
                cursor.execute("""
                    INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id)
                    VALUES (%s, %s, %s, %s, %s)
                """, (descripcion_meta, fecha_inicio, fecha_fin, estado, alumno_id))
        
        conn.commit()
        cursor.close()
        
        flash('Rutina creada exitosamente', 'success')
        return redirect(url_for('rutinas.index', alumno_id=alumno_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al crear rutina: {str(e)}")
        flash(f'Error al crear rutina: {str(e)}', 'danger')
        return redirect(url_for('rutinas.nueva_rutina', alumno_id=alumno_id))

@rutinas.route('/detalle/<int:rutina_id>', methods=['GET'])
@login_required
def detalle_rutina(rutina_id):
    """Muestra los detalles de una rutina específica"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la rutina
        cursor.execute("""
            SELECT r.*, u.nombres, u.apellidos
            FROM Rutina r
            JOIN Usuario u ON r.Usuario_id = u.id
            WHERE r.id = %s
        """, (rutina_id,))
        
        rutina = cursor.fetchone()
        
        if not rutina:
            flash('Rutina no encontrada', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Verificar permisos si es instructor
        if current_user.is_instructor():
            cursor.execute("""
                SELECT ci.id 
                FROM Cliente_Instructor ci 
                WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
            """, (rutina['Usuario_id'], current_user.id))
            
            if not cursor.fetchone():
                flash('No tienes permiso para ver esta rutina', 'danger')
                return redirect(url_for('alumnos.index'))
        # Si es cliente, verificar que la rutina le pertenece
        elif current_user.id != rutina['Usuario_id']:
            flash('No tienes permiso para ver esta rutina', 'danger')
            return redirect(url_for('dieta.index'))
        
        # Obtener ejercicios de la rutina
        cursor.execute("""
            SELECT er.orden, e.*
            FROM Ejercicio_Rutina er
            JOIN Ejercicio e ON er.Ejercicio_id = e.id
            WHERE er.Rutina_id = %s
            ORDER BY er.orden
        """, (rutina_id,))
        
        ejercicios = cursor.fetchall()
        
        cursor.close()
        
        return render_template('rutinas/detalle.html', 
                             rutina=rutina,
                             ejercicios=ejercicios)
        
    except Exception as e:
        current_app.logger.error(f"Error al mostrar detalles de rutina: {str(e)}")
        flash(f'Error al cargar detalles de la rutina: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@rutinas.route('/editar/<int:rutina_id>', methods=['GET', 'POST'])
@login_required
def editar_rutina(rutina_id):
    """Edita una rutina existente"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden editar rutinas', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la rutina
        cursor.execute("""
            SELECT r.*, u.nombres, u.apellidos, u.id as alumno_id
            FROM Rutina r
            JOIN Usuario u ON r.Usuario_id = u.id
            WHERE r.id = %s
        """, (rutina_id,))
        
        rutina = cursor.fetchone()
        
        if not rutina:
            flash('Rutina no encontrada', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Verificar permisos
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (rutina['Usuario_id'], current_user.id))
        
        if not cursor.fetchone():
            flash('No tienes permiso para editar esta rutina', 'danger')
            return redirect(url_for('alumnos.index'))
        
        if request.method == 'GET':
            # Obtener ejercicios de la rutina
            cursor.execute("""
                SELECT er.orden, e.*, er.id as er_id
                FROM Ejercicio_Rutina er
                JOIN Ejercicio e ON er.Ejercicio_id = e.id
                WHERE er.Rutina_id = %s
                ORDER BY er.orden
            """, (rutina_id,))
            
            ejercicios_rutina = cursor.fetchall()
            
            # Obtener todos los ejercicios
            cursor.execute("""
                SELECT * FROM Ejercicio
                ORDER BY nombre
            """)
            
            ejercicios = cursor.fetchall()
            
            # Obtener ejercicios ya asignados a la rutina
            ejercicios_ids = [e['id'] for e in ejercicios_rutina]
            
            cursor.close()
            
            return render_template('rutinas/editar.html', 
                                rutina=rutina,
                                ejercicios_rutina=ejercicios_rutina,
                                ejercicios=ejercicios,
                                ejercicios_ids=ejercicios_ids)
        
        # Procesar POST para actualizar rutina
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        
        # Validaciones básicas
        if not nombre:
            flash('El nombre de la rutina es obligatorio', 'warning')
            return redirect(url_for('rutinas.editar_rutina', rutina_id=rutina_id))
        
        # Actualizar rutina
        cursor.execute("""
            UPDATE Rutina SET
                nombre = %s,
                descripcion = %s
            WHERE id = %s
        """, (nombre, descripcion, rutina_id))
        
        # Eliminar ejercicios anteriores
        cursor.execute("""
            DELETE FROM Ejercicio_Rutina
            WHERE Rutina_id = %s
        """, (rutina_id,))
        
        # Procesar ejercicios seleccionados
        ejercicios = request.form.getlist('ejercicios[]')
        
        for i, ejercicio_id in enumerate(ejercicios, 1):
            cursor.execute("""
                INSERT INTO Ejercicio_Rutina (orden, Ejercicio_id, Rutina_id)
                VALUES (%s, %s, %s)
            """, (i, ejercicio_id, rutina_id))
        
        conn.commit()
        cursor.close()
        
        flash('Rutina actualizada exitosamente', 'success')
        return redirect(url_for('rutinas.detalle_rutina', rutina_id=rutina_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al editar rutina: {str(e)}")
        flash(f'Error al editar rutina: {str(e)}', 'danger')
        return redirect(url_for('rutinas.editar_rutina', rutina_id=rutina_id))

@rutinas.route('/eliminar/<int:rutina_id>', methods=['POST'])
@login_required
def eliminar_rutina(rutina_id):
    """Elimina una rutina existente"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden eliminar rutinas', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la rutina
        cursor.execute("""
            SELECT r.Usuario_id as alumno_id
            FROM Rutina r
            WHERE r.id = %s
        """, (rutina_id,))
        
        rutina = cursor.fetchone()
        
        if not rutina:
            flash('Rutina no encontrada', 'danger')
            return redirect(url_for('alumnos.index'))
        
        alumno_id = rutina['alumno_id']
        
        # Verificar permisos
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        if not cursor.fetchone():
            flash('No tienes permiso para eliminar esta rutina', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Eliminar ejercicios de la rutina
        cursor.execute("""
            DELETE FROM Ejercicio_Rutina
            WHERE Rutina_id = %s
        """, (rutina_id,))
        
        # Eliminar rutina
        cursor.execute("""
            DELETE FROM Rutina
            WHERE id = %s
        """, (rutina_id,))
        
        conn.commit()
        cursor.close()
        
        flash('Rutina eliminada exitosamente', 'success')
        return redirect(url_for('rutinas.index', alumno_id=alumno_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al eliminar rutina: {str(e)}")
        flash(f'Error al eliminar rutina: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@rutinas.route('/ejercicios', methods=['GET'])
@login_required
def lista_ejercicios():
    """Lista todos los ejercicios disponibles"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden acceder a esta sección', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM Ejercicio
            ORDER BY nombre
        """)
        
        ejercicios = cursor.fetchall()
        cursor.close()
        
        return render_template('rutinas/ejercicios.html', ejercicios=ejercicios)
        
    except Exception as e:
        current_app.logger.error(f"Error al listar ejercicios: {str(e)}")
        flash(f'Error al cargar ejercicios: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@rutinas.route('/ejercicios/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_ejercicio():
    """Crea un nuevo ejercicio"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden crear ejercicios', 'warning')
        return redirect(url_for('dieta.index'))
    
    if request.method == 'GET':
        return render_template('rutinas/nuevo_ejercicio.html')
    
    try:
        # Procesar POST para crear ejercicio
        nombre = request.form.get('nombre', '').strip()
        descripcion = request.form.get('descripcion', '').strip()
        series = int(request.form.get('series', 0))
        repeticiones = int(request.form.get('repeticiones', 0))
        tiempo_descanso = int(request.form.get('tiempo_descanso', 0))
        
        # Validaciones básicas
        if not nombre or series <= 0 or repeticiones <= 0 or tiempo_descanso <= 0:
            flash('Todos los campos son obligatorios y deben ser válidos', 'warning')
            return redirect(url_for('rutinas.nuevo_ejercicio'))
        
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Crear ejercicio
        cursor.execute("""
            INSERT INTO Ejercicio (nombre, descripcion, series, repeticiones, tiempo_descanso)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, descripcion, series, repeticiones, tiempo_descanso))
        
        conn.commit()
        cursor.close()
        
        flash('Ejercicio creado exitosamente', 'success')
        return redirect(url_for('rutinas.lista_ejercicios'))
        
    except Exception as e:
        current_app.logger.error(f"Error al crear ejercicio: {str(e)}")
        flash(f'Error al crear ejercicio: {str(e)}', 'danger')
        return redirect(url_for('rutinas.nuevo_ejercicio'))

@rutinas.route('/metas/nueva/<int:alumno_id>', methods=['GET', 'POST'])
@login_required
def nueva_meta(alumno_id):
    """Crea una nueva meta para un alumno"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden crear metas', 'warning')
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
                SELECT u.nombres, u.apellidos
                FROM Usuario u
                WHERE u.id = %s
            """, (alumno_id,))
            
            alumno = cursor.fetchone()
            cursor.close()
            
            if not alumno:
                flash('Alumno no encontrado', 'danger')
                return redirect(url_for('alumnos.index'))
            
            return render_template('rutinas/nueva_meta.html', 
                                 alumno=alumno,
                                 alumno_id=alumno_id)
        
        # Procesar POST para crear meta
        descripcion = request.form.get('descripcion', '').strip()
        fecha_inicio = request.form.get('fecha_inicio', '')
        fecha_fin = request.form.get('fecha_fin', '')
        estado = request.form.get('estado', 'En progreso')
        
        # Validaciones básicas
        if not descripcion or not fecha_inicio or not fecha_fin:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return redirect(url_for('rutinas.nueva_meta', alumno_id=alumno_id))
        
        # Crear meta
        cursor.execute("""
            INSERT INTO Meta (descripcion, fecha_inicio, fecha_fin, estado, Usuario_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (descripcion, fecha_inicio, fecha_fin, estado, alumno_id))
        
        conn.commit()
        cursor.close()
        
        flash('Meta creada exitosamente', 'success')
        return redirect(url_for('rutinas.index', alumno_id=alumno_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al crear meta: {str(e)}")
        flash(f'Error al crear meta: {str(e)}', 'danger')
        return redirect(url_for('rutinas.nueva_meta', alumno_id=alumno_id))

@rutinas.route('/metas/editar/<int:meta_id>', methods=['GET', 'POST'])
@login_required
def editar_meta(meta_id):
    """Edita una meta existente"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden editar metas', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la meta
        cursor.execute("""
            SELECT m.*, u.nombres, u.apellidos, u.id as alumno_id
            FROM Meta m
            JOIN Usuario u ON m.Usuario_id = u.id
            WHERE m.id = %s
        """, (meta_id,))
        
        meta = cursor.fetchone()
        
        if not meta:
            flash('Meta no encontrada', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Verificar permisos
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (meta['Usuario_id'], current_user.id))
        
        if not cursor.fetchone():
            flash('No tienes permiso para editar esta meta', 'danger')
            return redirect(url_for('alumnos.index'))
        
        if request.method == 'GET':
            cursor.close()
            
            # Formatear fechas para el formulario
            if meta['fecha_inicio']:
                meta['fecha_inicio'] = meta['fecha_inicio'].strftime('%Y-%m-%d')
            if meta['fecha_fin']:
                meta['fecha_fin'] = meta['fecha_fin'].strftime('%Y-%m-%d')
            
            return render_template('rutinas/editar_meta.html', meta=meta)
        
        # Procesar POST para actualizar meta
        descripcion = request.form.get('descripcion', '').strip()
        fecha_inicio = request.form.get('fecha_inicio', '')
        fecha_fin = request.form.get('fecha_fin', '')
        estado = request.form.get('estado', 'En progreso')
        
        # Validaciones básicas
        if not descripcion or not fecha_inicio or not fecha_fin:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return redirect(url_for('rutinas.editar_meta', meta_id=meta_id))
        
        # Actualizar meta
        cursor.execute("""
            UPDATE Meta SET
                descripcion = %s,
                fecha_inicio = %s,
                fecha_fin = %s,
                estado = %s
            WHERE id = %s
        """, (descripcion, fecha_inicio, fecha_fin, estado, meta_id))
        
        conn.commit()
        cursor.close()
        
        flash('Meta actualizada exitosamente', 'success')
        return redirect(url_for('rutinas.index', alumno_id=meta['alumno_id']))
        
    except Exception as e:
        current_app.logger.error(f"Error al editar meta: {str(e)}")
        flash(f'Error al editar meta: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@rutinas.route('/metas/eliminar/<int:meta_id>', methods=['POST'])
@login_required
def eliminar_meta(meta_id):
    """Elimina una meta existente"""
    if not current_user.is_instructor():
        flash('Solo los instructores pueden eliminar metas', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener información de la meta
        cursor.execute("""
            SELECT m.Usuario_id as alumno_id
            FROM Meta m
            WHERE m.id = %s
        """, (meta_id,))
        
        meta = cursor.fetchone()
        
        if not meta:
            flash('Meta no encontrada', 'danger')
            return redirect(url_for('alumnos.index'))
        
        alumno_id = meta['alumno_id']
        
        # Verificar permisos
        cursor.execute("""
            SELECT ci.id 
            FROM Cliente_Instructor ci 
            WHERE ci.Usuario_id = %s AND ci.Usuario_2_id = %s
        """, (alumno_id, current_user.id))
        
        if not cursor.fetchone():
            flash('No tienes permiso para eliminar esta meta', 'danger')
            return redirect(url_for('alumnos.index'))
        
        # Eliminar meta
        cursor.execute("""
            DELETE FROM Meta
            WHERE id = %s
        """, (meta_id,))
        
        conn.commit()
        cursor.close()
        
        flash('Meta eliminada exitosamente', 'success')
        return redirect(url_for('rutinas.index', alumno_id=alumno_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al eliminar meta: {str(e)}")
        flash(f'Error al eliminar meta: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index')) 