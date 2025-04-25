from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.horario import Horario
from app.models.servicio import Servicio
from app.models.usuario import Usuario
from app.extensions import db
from datetime import datetime, time

horario_bp = Blueprint('horario', __name__, url_prefix='/horarios')

@horario_bp.route('/servicio/<int:servicio_id>')
@login_required
def lista_horarios(servicio_id):
    """Lista los horarios de un servicio específico"""
    servicio = Servicio.query.get_or_404(servicio_id)
    return render_template('horario/lista.html', servicio=servicio)

@horario_bp.route('/nuevo/<int:servicio_id>', methods=['GET', 'POST'])
@login_required
def nuevo_horario(servicio_id):
    """Agregar un nuevo horario a un servicio"""
    servicio = Servicio.query.get_or_404(servicio_id)
    
    if request.method == 'POST':
        try:
            hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
            hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()
            
            horario = Horario(
                servicio_id=servicio_id,
                dia_semana=int(request.form['dia_semana']),
                hora_inicio=hora_inicio,
                hora_fin=hora_fin,
                cupo_maximo=int(request.form['cupo_maximo'])
            )
            
            db.session.add(horario)
            db.session.commit()
            flash('Horario agregado exitosamente', 'success')
            return redirect(url_for('horario.lista_horarios', servicio_id=servicio_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el horario: {str(e)}', 'error')
    
    return render_template('horario/form.html', servicio=servicio, horario=None)

@horario_bp.route('/editar/<int:horario_id>', methods=['GET', 'POST'])
@login_required
def editar_horario(horario_id):
    """Editar un horario existente"""
    horario = Horario.query.get_or_404(horario_id)
    servicio = horario.servicio
    
    if request.method == 'POST':
        try:
            hora_inicio = datetime.strptime(request.form['hora_inicio'], '%H:%M').time()
            hora_fin = datetime.strptime(request.form['hora_fin'], '%H:%M').time()
            
            horario.dia_semana = int(request.form['dia_semana'])
            horario.hora_inicio = hora_inicio
            horario.hora_fin = hora_fin
            horario.cupo_maximo = int(request.form['cupo_maximo'])
            
            db.session.commit()
            flash('Horario actualizado exitosamente', 'success')
            return redirect(url_for('horario.lista_horarios', servicio_id=servicio.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el horario: {str(e)}', 'error')
    
    return render_template('horario/form.html', servicio=servicio, horario=horario)

@horario_bp.route('/eliminar/<int:horario_id>', methods=['POST'])
@login_required
def eliminar_horario(horario_id):
    """Eliminar un horario"""
    horario = Horario.query.get_or_404(horario_id)
    servicio_id = horario.servicio_id
    
    try:
        db.session.delete(horario)
        db.session.commit()
        flash('Horario eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el horario: {str(e)}', 'error')
    
    return redirect(url_for('horario.lista_horarios', servicio_id=servicio_id))

@horario_bp.route('/disponibilidad/<int:horario_id>')
def disponibilidad(horario_id):
    """Obtener la disponibilidad de un horario"""
    horario = Horario.query.get_or_404(horario_id)
    disponibles = horario.cupo_maximo - len(horario.reservas)
    return jsonify({
        'cupo_maximo': horario.cupo_maximo,
        'disponibles': disponibles,
        'ocupados': len(horario.reservas)
    }) 