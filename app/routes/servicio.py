from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.servicio import Servicio, HorarioServicio, Certificacion, Testimonio
from app.models.instructor import Instructor
from app.extensions import db
from datetime import datetime, time
import os
from app.forms.horario import HorarioForm

servicio_bp = Blueprint('servicio', __name__, url_prefix='/servicios')

@servicio_bp.route('/perfil')
@login_required
def perfil_instructor():
    """Muestra el perfil público del instructor con sus servicios y certificaciones"""
    instructor = current_user
    return render_template('servicio/perfil.html', 
                         instructor=instructor,
                         servicios=instructor.servicios,
                         certificaciones=instructor.certificaciones,
                         testimonios=instructor.testimonios)

@servicio_bp.route('/')
@login_required
def lista_servicios():
    """Lista todos los servicios del instructor"""
    servicios = [s for s in current_user.servicios if s.activo]
    return render_template('servicio/lista.html', servicios=servicios)

@servicio_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_servicio():
    """Agregar un nuevo servicio"""
    if request.method == 'POST':
        try:
            servicio = Servicio(
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                precio=float(request.form['precio']),
                duracion=int(request.form['duracion']),
                instructor_id=current_user.id
            )
            servicio.capacidad_maxima = int(request.form['capacidad_maxima'])
            servicio.activo = bool(request.form.get('activo', False))
            
            # Procesar horarios
            dias = request.form.getlist('dia_semana[]')
            horas_inicio = request.form.getlist('hora_inicio[]')
            horas_fin = request.form.getlist('hora_fin[]')
            cupos_maximos = request.form.getlist('cupo_maximo[]')
            
            for dia, inicio, fin, cupo in zip(dias, horas_inicio, horas_fin, cupos_maximos):
                horario = HorarioServicio(
                    dia_semana=int(dia),
                    hora_inicio=datetime.strptime(inicio, '%H:%M').time(),
                    hora_fin=datetime.strptime(fin, '%H:%M').time(),
                    cupo_maximo=int(cupo)
                )
                servicio.horarios.append(horario)
            
            db.session.add(servicio)
            db.session.commit()
            flash('Servicio agregado exitosamente', 'success')
            return redirect(url_for('servicio.lista_servicios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el servicio: {str(e)}', 'danger')
    
    return render_template('servicio/nuevo.html')

@servicio_bp.route('/<int:servicio_id>/editar', methods=['GET', 'POST'])
@login_required
def editar_servicio(servicio_id):
    """Editar un servicio existente"""
    servicio = Servicio.query.get_or_404(servicio_id)
    
    if servicio.instructor_id != current_user.id:
        flash('No tienes permiso para editar este servicio', 'danger')
        return redirect(url_for('servicio.lista_servicios'))
    
    if request.method == 'POST':
        try:
            servicio.nombre = request.form['nombre']
            servicio.descripcion = request.form['descripcion']
            servicio.precio = float(request.form['precio'])
            servicio.duracion = int(request.form['duracion'])
            servicio.capacidad_maxima = int(request.form['capacidad_maxima'])
            servicio.activo = bool(request.form.get('activo', False))
            
            # Eliminar horarios existentes
            for horario in servicio.horarios:
                db.session.delete(horario)
            
            # Procesar nuevos horarios
            dias = request.form.getlist('dia_semana[]')
            horas_inicio = request.form.getlist('hora_inicio[]')
            horas_fin = request.form.getlist('hora_fin[]')
            cupos_maximos = request.form.getlist('cupo_maximo[]')
            
            for dia, inicio, fin, cupo in zip(dias, horas_inicio, horas_fin, cupos_maximos):
                horario = HorarioServicio(
                    dia_semana=int(dia),
                    hora_inicio=datetime.strptime(inicio, '%H:%M').time(),
                    hora_fin=datetime.strptime(fin, '%H:%M').time(),
                    cupo_maximo=int(cupo)
                )
                servicio.horarios.append(horario)
            
            db.session.commit()
            flash('Servicio actualizado exitosamente', 'success')
            return redirect(url_for('servicio.lista_servicios'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el servicio: {str(e)}', 'danger')
    
    return render_template('servicio/editar.html', servicio=servicio)

@servicio_bp.route('/<int:servicio_id>/eliminar')
@login_required
def eliminar_servicio(servicio_id):
    """Eliminar un servicio"""
    servicio = Servicio.query.get_or_404(servicio_id)
    
    if servicio.instructor_id != current_user.id:
        flash('No tienes permiso para eliminar este servicio', 'danger')
        return redirect(url_for('servicio.lista_servicios'))
        
    servicio.activo = False
    db.session.commit()
    flash('Servicio eliminado exitosamente', 'success')
    return redirect(url_for('servicio.lista_servicios'))

@servicio_bp.route('/servicios/<int:servicio_id>/horarios')
def lista_horarios(servicio_id):
    servicio = Servicio.query.get_or_404(servicio_id)
    horarios = HorarioServicio.query.filter_by(servicio_id=servicio_id).order_by(HorarioServicio.dia_semana, HorarioServicio.hora_inicio).all()
    return render_template('servicio/horarios.html', servicio=servicio, horarios=horarios)

@servicio_bp.route('/servicios/<int:servicio_id>/horarios/nuevo', methods=['GET', 'POST'])
def nuevo_horario(servicio_id):
    servicio = Servicio.query.get_or_404(servicio_id)
    form = HorarioForm()
    
    if form.validate_on_submit():
        try:
            # Crear un horario para cada día seleccionado
            for dia in form.dias_semana.data:
                horario = HorarioServicio(
                    servicio_id=servicio_id,
                    dia_semana=int(dia),
                    hora_inicio=form.hora_inicio.data,
                    hora_fin=form.hora_fin.data,
                    cupo_maximo=form.cupo_maximo.data
                )
                db.session.add(horario)
            
            db.session.commit()
            flash('Horarios creados exitosamente', 'success')
            return redirect(url_for('servicio.lista_horarios', servicio_id=servicio_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear los horarios: {str(e)}', 'danger')
        
    return render_template('servicio/nuevo_horario.html', form=form, servicio=servicio)

@servicio_bp.route('/horarios/<int:horario_id>/editar', methods=['GET', 'POST'])
def editar_horario(horario_id):
    horario = HorarioServicio.query.get_or_404(horario_id)
    form = HorarioForm(obj=horario)
    
    if request.method == 'POST':
        horario.dia_semana = int(request.form['dia_semana'])
        horario.hora_inicio = form.hora_inicio.data
        horario.hora_fin = form.hora_fin.data
        horario.cupo_maximo = form.cupo_maximo.data
        db.session.commit()
        flash('Horario actualizado exitosamente', 'success')
        return redirect(url_for('servicio.lista_horarios', servicio_id=horario.servicio_id))
    
    return render_template('servicio/editar_horario.html', form=form, horario=horario)

@servicio_bp.route('/horarios/<int:horario_id>/eliminar', methods=['POST'])
def eliminar_horario(horario_id):
    horario = HorarioServicio.query.get_or_404(horario_id)
    servicio_id = horario.servicio_id
    
    db.session.delete(horario)
    db.session.commit()
    flash('Horario eliminado exitosamente', 'success')
    return redirect(url_for('servicio.lista_horarios', servicio_id=servicio_id))

@servicio_bp.route('/certificacion/agregar', methods=['GET', 'POST'])
@login_required
def agregar_certificacion():
    """Agregar una nueva certificación"""
    if request.method == 'POST':
        try:
            # Procesar imagen si se subió una
            imagen = request.files.get('imagen')
            ruta_imagen = None
            
            if imagen:
                filename = f"cert_{current_user.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{imagen.filename.split('.')[-1]}"
                imagen.save(os.path.join('app/static/uploads/certificaciones', filename))
                ruta_imagen = f'uploads/certificaciones/{filename}'
            
            certificacion = Certificacion(
                instructor_id=current_user.id,
                titulo=request.form['titulo'],
                institucion=request.form['institucion'],
                fecha_obtencion=datetime.strptime(request.form['fecha_obtencion'], '%Y-%m-%d'),
                descripcion=request.form['descripcion'],
                imagen=ruta_imagen
            )
            
            db.session.add(certificacion)
            db.session.commit()
            flash('Certificación agregada exitosamente', 'success')
            return redirect(url_for('servicio.perfil_instructor'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar la certificación: {str(e)}', 'danger')
    
    return render_template('servicio/agregar_certificacion.html')

@servicio_bp.route('/testimonio/agregar/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def agregar_testimonio(cliente_id):
    """Agregar un nuevo testimonio"""
    if request.method == 'POST':
        try:
            # Procesar imágenes
            imagen_antes = request.files.get('imagen_antes')
            imagen_despues = request.files.get('imagen_despues')
            ruta_antes = None
            ruta_despues = None
            
            if imagen_antes:
                filename = f"antes_{cliente_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{imagen_antes.filename.split('.')[-1]}"
                imagen_antes.save(os.path.join('app/static/uploads/testimonios', filename))
                ruta_antes = f'uploads/testimonios/{filename}'
            
            if imagen_despues:
                filename = f"despues_{cliente_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{imagen_despues.filename.split('.')[-1]}"
                imagen_despues.save(os.path.join('app/static/uploads/testimonios', filename))
                ruta_despues = f'uploads/testimonios/{filename}'
            
            testimonio = Testimonio(
                instructor_id=current_user.id,
                cliente_id=cliente_id,
                contenido=request.form['contenido'],
                calificacion=int(request.form['calificacion']),
                imagen_antes=ruta_antes,
                imagen_despues=ruta_despues
            )
            
            db.session.add(testimonio)
            db.session.commit()
            flash('Testimonio agregado exitosamente', 'success')
            return redirect(url_for('servicio.perfil_instructor'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el testimonio: {str(e)}', 'danger')
    
    return render_template('servicio/agregar_testimonio.html', cliente_id=cliente_id) 