from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.dieta import Dieta, ComidaDieta
from app.models.cliente import Cliente
from app.models.rutina import Rutina
from app.extensions import db
from datetime import datetime, time

dieta_bp = Blueprint('dieta', __name__, url_prefix='/dietas')

@dieta_bp.route('/cliente/<int:cliente_id>')
@login_required
def lista_dietas(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    dietas = Dieta.query.filter_by(cliente_id=cliente_id).order_by(Dieta.fecha_inicio.desc()).all()
    return render_template('dieta/lista.html', cliente=cliente, dietas=dietas)

@dieta_bp.route('/crear/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def crear(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    rutina_id = request.args.get('rutina_id', type=int)
    rutina = None
    if rutina_id:
        rutina = Rutina.query.get_or_404(rutina_id)
        if rutina.cliente_id != cliente_id:
            flash('La rutina no pertenece a este cliente', 'danger')
            return redirect(url_for('rutina.lista_rutinas', cliente_id=cliente_id))
    
    if request.method == 'POST':
        try:
            nueva_dieta = Dieta(
                cliente_id=cliente_id,
                instructor_id=current_user.id,
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                fecha_inicio=datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date(),
                calorias_diarias=request.form.get('calorias_diarias', type=int)
            )
            
            db.session.add(nueva_dieta)
            
            # Si se está creando desde una rutina, asociar la dieta
            if rutina:
                rutina.dieta = nueva_dieta
            
            db.session.commit()
            
            flash('Dieta creada exitosamente', 'success')
            if rutina:
                return redirect(url_for('rutina.lista_rutinas', cliente_id=cliente_id))
            return redirect(url_for('dieta.editar_comidas', dieta_id=nueva_dieta.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la dieta: {str(e)}', 'danger')
    
    return render_template('dieta/crear.html', cliente=cliente, rutina=rutina)

@dieta_bp.route('/editar/<int:dieta_id>', methods=['GET', 'POST'])
@login_required
def editar(dieta_id):
    dieta = Dieta.query.get_or_404(dieta_id)
    
    if dieta.instructor_id != current_user.id:
        flash('No tienes permiso para editar esta dieta', 'danger')
        return redirect(url_for('dieta.lista_dietas', cliente_id=dieta.cliente_id))
    
    if request.method == 'POST':
        try:
            dieta.titulo = request.form['titulo']
            dieta.descripcion = request.form['descripcion']
            dieta.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            dieta.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
            dieta.calorias_diarias = request.form.get('calorias_diarias', type=int)
            dieta.activa = 'activa' in request.form
            
            db.session.commit()
            flash('Dieta actualizada exitosamente', 'success')
            
            # Si la dieta está asociada a una rutina, redirigir a la lista de rutinas
            if dieta.rutina:
                return redirect(url_for('rutina.lista_rutinas', cliente_id=dieta.cliente_id))
            return redirect(url_for('dieta.lista_dietas', cliente_id=dieta.cliente_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la dieta: {str(e)}', 'danger')
    
    return render_template('dieta/editar.html', dieta=dieta)

@dieta_bp.route('/comidas/<int:dieta_id>', methods=['GET', 'POST'])
@login_required
def editar_comidas(dieta_id):
    dieta = Dieta.query.get_or_404(dieta_id)
    
    if dieta.instructor_id != current_user.id:
        flash('No tienes permiso para editar esta dieta', 'danger')
        return redirect(url_for('dieta.lista_dietas', cliente_id=dieta.cliente_id))
    
    if request.method == 'POST':
        try:
            comida = ComidaDieta(
                dieta_id=dieta_id,
                tipo_comida=request.form['tipo_comida'],
                hora=datetime.strptime(request.form['hora'], '%H:%M').time(),
                descripcion=request.form['descripcion'],
                calorias=request.form.get('calorias', type=int),
                proteinas=request.form.get('proteinas', type=float),
                carbohidratos=request.form.get('carbohidratos', type=float),
                grasas=request.form.get('grasas', type=float)
            )
            
            db.session.add(comida)
            db.session.commit()
            flash('Comida agregada exitosamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar comida: {str(e)}', 'danger')
    
    return render_template('dieta/comidas.html', dieta=dieta)

@dieta_bp.route('/eliminar_comida/<int:comida_id>')
@login_required
def eliminar_comida(comida_id):
    comida = ComidaDieta.query.get_or_404(comida_id)
    dieta_id = comida.dieta_id
    
    if comida.dieta.instructor_id != current_user.id:
        flash('No tienes permiso para eliminar esta comida', 'danger')
        return redirect(url_for('dieta.lista_dietas', cliente_id=comida.dieta.cliente_id))
    
    try:
        db.session.delete(comida)
        db.session.commit()
        flash('Comida eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar comida: {str(e)}', 'danger')
    
    return redirect(url_for('dieta.editar_comidas', dieta_id=dieta_id))

@dieta_bp.route('/eliminar/<int:dieta_id>')
@login_required
def eliminar(dieta_id):
    dieta = Dieta.query.get_or_404(dieta_id)
    cliente_id = dieta.cliente_id
    rutina = dieta.rutina
    
    if dieta.instructor_id != current_user.id:
        flash('No tienes permiso para eliminar esta dieta', 'danger')
        return redirect(url_for('dieta.lista_dietas', cliente_id=cliente_id))
    
    try:
        # Si la dieta está asociada a una rutina, desasociarla
        if rutina:
            rutina.dieta = None
        db.session.delete(dieta)
        db.session.commit()
        flash('Dieta eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar dieta: {str(e)}', 'danger')
    
    if rutina:
        return redirect(url_for('rutina.lista_rutinas', cliente_id=cliente_id))
    return redirect(url_for('dieta.lista_dietas', cliente_id=cliente_id)) 