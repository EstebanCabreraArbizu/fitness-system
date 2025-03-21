from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.meta import Meta, HistorialMedida
from app.models.rutina import Rutina
from app.extensions import db
from flask_login import login_required, current_user
from datetime import datetime

meta_bp = Blueprint('meta', __name__, url_prefix='/metas')

@meta_bp.route('/rutina/<int:rutina_id>')
@login_required
def lista_metas(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)
    
    # Verificar que el instructor es el propietario de la rutina o el cliente
    if rutina.instructor_id != current_user.id:
        flash('No tienes permiso para acceder a estas metas', 'danger')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    # Obtener todas las metas asociadas a esta rutina
    metas = Meta.query.filter_by(rutina_id=rutina_id).all()
    
    return render_template('meta/lista.html', 
                         metas=metas, 
                         rutina=rutina)

@meta_bp.route('/crear/<int:rutina_id>', methods=['GET', 'POST'])
@login_required
def crear(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)
    
    # Verificar permisos
    if rutina.instructor_id != current_user.id:
        flash('No tienes permiso para crear metas para esta rutina', 'danger')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    if request.method == 'POST':
        try:
            nueva_meta = Meta(
                rutina_id=rutina_id,
                tipo_medida=request.form['tipo_medida'],
                medida_inicial=float(request.form['medida_inicial']),
                medida_objetivo=float(request.form['medida_objetivo']),
                unidad=request.form['unidad'],
                notas=request.form['notas']
            )
            
            db.session.add(nueva_meta)
            
            # Crear primer registro en el historial
            primer_historial = HistorialMedida(
                meta=nueva_meta,  # SQLAlchemy maneja la asignación del ID
                medida=float(request.form['medida_inicial']),
                notas='Medida inicial'
            )
            
            db.session.add(primer_historial)
            db.session.commit()
            
            flash('Meta creada exitosamente', 'success')
            return redirect(url_for('meta.lista_metas', rutina_id=rutina_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la meta: {str(e)}', 'danger')
    
    # Opciones para tipos de medidas
    tipos_medidas = [
        ('Brazo', 'cm'), ('Pecho', 'cm'), ('Espalda', 'cm'), 
        ('Cintura', 'cm'), ('Cadera', 'cm'), ('Muslo', 'cm'), 
        ('Pantorrilla', 'cm'), ('Peso', 'kg'), ('Porcentaje grasa', '%'),
        ('Fuerza press banca', 'kg'), ('Fuerza sentadilla', 'kg'), 
        ('Fuerza peso muerto', 'kg'), ('VO2 Max', 'ml/kg/min')
    ]
    
    return render_template('meta/crear.html', 
                         rutina=rutina,
                         tipos_medidas=tipos_medidas)

@meta_bp.route('/editar/<int:meta_id>', methods=['GET', 'POST'])
@login_required
def editar(meta_id):
    meta = Meta.query.get_or_404(meta_id)
    rutina = meta.rutina
    
    # Verificar permisos
    if rutina.instructor_id != current_user.id:
        flash('No tienes permiso para editar esta meta', 'danger')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    if request.method == 'POST':
        try:
            meta.tipo_medida = request.form['tipo_medida']
            meta.medida_inicial = float(request.form['medida_inicial'])
            meta.medida_objetivo = float(request.form['medida_objetivo'])
            meta.unidad = request.form['unidad']
            meta.notas = request.form['notas']
            
            # Actualizar estado de logro si se marca como alcanzado
            if 'logrado' in request.form:
                meta.logrado = True
                meta.fecha_logro = datetime.utcnow()
            else:
                meta.logrado = False
                meta.fecha_logro = None
            
            db.session.commit()
            flash('Meta actualizada exitosamente', 'success')
            return redirect(url_for('meta.lista_metas', rutina_id=meta.rutina_id))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la meta: {str(e)}', 'danger')
    
    # Opciones para tipos de medidas
    tipos_medidas = [
        ('Brazo', 'cm'), ('Pecho', 'cm'), ('Espalda', 'cm'), 
        ('Cintura', 'cm'), ('Cadera', 'cm'), ('Muslo', 'cm'), 
        ('Pantorrilla', 'cm'), ('Peso', 'kg'), ('Porcentaje grasa', '%'),
        ('Fuerza press banca', 'kg'), ('Fuerza sentadilla', 'kg'), 
        ('Fuerza peso muerto', 'kg'), ('VO2 Max', 'ml/kg/min')
    ]
    
    return render_template('meta/editar.html', 
                         meta=meta,
                         rutina=rutina,
                         tipos_medidas=tipos_medidas)

@meta_bp.route('/historial/<int:meta_id>', methods=['GET', 'POST'])
@login_required
def historial(meta_id):
    meta = Meta.query.get_or_404(meta_id)
    rutina = meta.rutina
    
    # Verificar permisos
    if rutina.instructor_id != current_user.id:
        flash('No tienes permiso para ver este historial', 'danger')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    if request.method == 'POST':
        try:
            # Agregar nueva medida al historial
            nueva_medida = HistorialMedida(
                meta_id=meta_id,
                medida=float(request.form['medida']),
                notas=request.form['notas']
            )
            
            db.session.add(nueva_medida)
            
            # Comprobar si se ha alcanzado el objetivo
            if not meta.logrado and nueva_medida.medida >= meta.medida_objetivo:
                meta.logrado = True
                meta.fecha_logro = datetime.utcnow()
                flash('¡Felicidades! Se ha alcanzado el objetivo', 'success')
            
            db.session.commit()
            flash('Medida registrada exitosamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la medida: {str(e)}', 'danger')
    
    # Obtener historial ordenado por fecha
    historial = HistorialMedida.query.filter_by(meta_id=meta_id).order_by(HistorialMedida.fecha.desc()).all()
    
    # Calcular el progreso aquí
    if historial:
        ultima_medida = historial[0].medida
    else:
        ultima_medida = meta.medida_inicial
        
    if meta.medida_objetivo != meta.medida_inicial:
        progreso_raw = ((ultima_medida - meta.medida_inicial) / (meta.medida_objetivo - meta.medida_inicial) * 100)
        progreso = max(0, min(100, round(progreso_raw)))
    else:
        progreso = 0
    
    return render_template('meta/historial.html',
                         meta=meta,
                         rutina=rutina,
                         historial=historial,
                         progreso=progreso)

@meta_bp.route('/eliminar/<int:meta_id>')
@login_required
def eliminar(meta_id):
    meta = Meta.query.get_or_404(meta_id)
    rutina_id = meta.rutina_id
    rutina = meta.rutina
    
    # Verificar permisos
    if rutina.instructor_id != current_user.id:
        flash('No tienes permiso para eliminar esta meta', 'danger')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    try:
        db.session.delete(meta)
        db.session.commit()
        flash('Meta eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la meta: {str(e)}', 'danger')
    
    return redirect(url_for('meta.lista_metas', rutina_id=rutina_id)) 