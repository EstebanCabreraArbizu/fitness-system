from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.cliente import Cliente
from app.models.medicion import Medicion
from app.models.meta import Meta
from app.models.historial_medida import HistorialMedida
from app.extensions import db
from datetime import datetime

cliente = Blueprint('cliente', __name__)

@cliente.route('/perfil', methods=['GET'])
@login_required
def perfil():
    return render_template('cliente/perfil.html', cliente=current_user)

@cliente.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        current_user.nombres = request.form['nombres']
        current_user.apellidos = request.form['apellidos']
        current_user.telefono = request.form['telefono']
        current_user.fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
        current_user.genero = request.form['genero']
        current_user.altura = float(request.form['altura'])
        
        db.session.commit()
        flash('Perfil actualizado exitosamente', 'success')
        return redirect(url_for('cliente.perfil'))
        
    return render_template('cliente/editar_perfil.html', cliente=current_user)

@cliente.route('/mediciones', methods=['GET'])
@login_required
def lista_mediciones():
    mediciones = Medicion.query.filter_by(cliente_id=current_user.id).order_by(Medicion.fecha.desc()).all()
    return render_template('cliente/mediciones.html', mediciones=mediciones)

@cliente.route('/mediciones/agregar', methods=['GET', 'POST'])
@login_required
def agregar_medicion():
    if request.method == 'POST':
        medicion = Medicion(
            cliente_id=current_user.id,
            fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d').date(),
            peso=float(request.form['peso']),
            masa_muscular=float(request.form['masa_muscular']),
            masa_grasa=float(request.form['masa_grasa']),
            porcentaje_grasa=float(request.form['porcentaje_grasa']),
            circunferencia_cintura=float(request.form['circunferencia_cintura']),
            circunferencia_cadera=float(request.form['circunferencia_cadera']),
            notas=request.form['notas']
        )
        db.session.add(medicion)
        db.session.commit()
        flash('Medición agregada exitosamente', 'success')
        return redirect(url_for('cliente.lista_mediciones'))
        
    return render_template('cliente/agregar_medicion.html')

@cliente.route('/metas', methods=['GET'])
@login_required
def lista_metas():
    metas = Meta.query.filter_by(cliente_id=current_user.id).all()
    return render_template('cliente/metas.html', metas=metas)

@cliente.route('/metas/agregar', methods=['GET', 'POST'])
@login_required
def agregar_meta():
    if request.method == 'POST':
        try:
            meta = Meta(
                cliente_id=current_user.id,
                tipo_medida=request.form['tipo'],
                medida_inicial=float(request.form['valor_actual']),
                medida_objetivo=float(request.form['valor_objetivo']),
                unidad=request.form.get('unidad', 'kg'),  # Unidad por defecto
                notas=request.form.get('notas', '')
            )
            
            # Crear el primer registro en el historial
            db.session.add(meta)
            db.session.flush()  # Para obtener el ID de la meta
            
            # Registrar la medida inicial en el historial
            historial = HistorialMedida(
                meta_id=meta.id,
                medida=meta.medida_inicial,
                notas='Medida inicial'
            )
            db.session.add(historial)
            db.session.commit()
            
            flash('Meta agregada exitosamente', 'success')
            return redirect(url_for('cliente.lista_metas'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar la meta: {str(e)}', 'danger')
            return redirect(url_for('cliente.agregar_meta'))
    
    # Tipos de medidas disponibles con sus unidades
    tipos_medidas = [
        ('Peso', 'kg'),
        ('Masa Muscular', 'kg'),
        ('Masa Grasa', 'kg'),
        ('Porcentaje Grasa', '%'),
        ('Circunferencia Cintura', 'cm'),
        ('Circunferencia Cadera', 'cm'),
        ('Brazo', 'cm'),
        ('Pecho', 'cm'),
        ('Muslo', 'cm'),
        ('Pantorrilla', 'cm')
    ]
    
    return render_template('cliente/agregar_meta.html', tipos_medidas=tipos_medidas) 