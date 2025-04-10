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

@dieta_bp.route('/crear', methods=['GET', 'POST'])
@dieta_bp.route('/crear/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def crear(cliente_id=None):
    rutina_id = request.args.get('rutina_id', type=int)
    
    if rutina_id:
        rutina = Rutina.query.get_or_404(rutina_id)
        cliente = rutina.cliente
        cliente_id = cliente.id
    elif cliente_id:
        cliente = Cliente.query.get_or_404(cliente_id)
        rutina = None
    else:
        flash('Se requiere un cliente o una rutina para crear una dieta', 'danger')
        return redirect(url_for('client.index'))
    
    if request.method == 'POST':
        try:
            nueva_dieta = Dieta(
                cliente_id=cliente_id,
                instructor_id=current_user.id,
                nombre=request.form['nombre'],
                descripcion=request.form['descripcion'],
                fecha_inicio=datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date(),
                fecha_fin=datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date(),
                calorias_diarias=request.form.get('calorias_diarias', type=int),
                proteinas=request.form.get('proteinas', type=float, default=0),
                carbohidratos=request.form.get('carbohidratos', type=float, default=0),
                grasas=request.form.get('grasas', type=float, default=0)
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
            dieta.nombre = request.form['nombre']
            dieta.descripcion = request.form['descripcion']
            dieta.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d').date()
            dieta.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d').date()
            dieta.calorias_diarias = request.form.get('calorias_diarias', type=int)
            dieta.proteinas = request.form.get('proteinas', type=float)
            dieta.carbohidratos = request.form.get('carbohidratos', type=float)
            dieta.grasas = request.form.get('grasas', type=float)
            dieta.notas = request.form.get('notas')
            
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
            # Obtener los arrays de datos de las comidas
            tipos_comida = request.form.getlist('tipo_comida[]')
            horas = request.form.getlist('hora[]')
            descripciones = request.form.getlist('descripcion[]')
            calorias = request.form.getlist('calorias[]')
            proteinas = request.form.getlist('proteinas[]')
            carbohidratos = request.form.getlist('carbohidratos[]')
            grasas = request.form.getlist('grasas[]')
            
            # Procesar cada comida
            for i in range(len(tipos_comida)):
                # Obtener los días seleccionados para esta comida
                dias = []
                for dia in range(1, 8):
                    if request.form.get(f'dias[{i}][{dia}]'):
                        dias.append(dia)
                
                # Crear la comida
                comida = ComidaDieta(
                    dieta_id=dieta_id,
                    tipo_comida=tipos_comida[i],
                    hora=datetime.strptime(horas[i], '%H:%M').time(),
                    descripcion=descripciones[i],
                    calorias=int(calorias[i]),
                    proteinas=float(proteinas[i]),
                    carbohidratos=float(carbohidratos[i]),
                    grasas=float(grasas[i]),
                    lunes=1 in dias,
                    martes=2 in dias,
                    miercoles=3 in dias,
                    jueves=4 in dias,
                    viernes=5 in dias,
                    sabado=6 in dias,
                    domingo=7 in dias
                )
                
                db.session.add(comida)
            
            db.session.commit()
            flash('Comidas agregadas exitosamente', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar comidas: {str(e)}', 'danger')
    
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