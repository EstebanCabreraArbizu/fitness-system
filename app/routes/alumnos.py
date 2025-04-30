from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.user import User
import os
import time

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
                   (SELECT COUNT(*) FROM Dieta WHERE Usuario_id = u.id AND Usuario_2_id = %s) as num_dietas
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
        current_app.logger.error(f"Error al listar alumnos: {str(e)}")
        flash(f'Error al cargar la lista de alumnos: {str(e)}', 'danger')
        return render_template('alumnos/index.html', alumnos=[])

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
        
        cursor.close()
        
        return render_template('alumnos/detalles.html', 
                             alumno=alumno,
                             medidas=medidas,
                             rutinas=rutinas,
                             metas=metas,
                             dietas=dietas)
        
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