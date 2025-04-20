from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.medicion import Medicion
from app.models.cliente import Cliente
from app.extensions import db
from datetime import datetime

medicion_bp = Blueprint('medicion', __name__, url_prefix='/mediciones')

@medicion_bp.route('/cliente/<int:cliente_id>')
@login_required
def lista_mediciones(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    mediciones = Medicion.query.filter_by(cliente_id=cliente_id).order_by(Medicion.fecha.desc()).all()
    return render_template('medicion/lista.html', cliente=cliente, mediciones=mediciones)

@medicion_bp.route('/agregar/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def agregar_medicion(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    if request.method == 'POST':
        try:
            # Crear nueva medición
            nueva_medicion = Medicion(
                cliente_id=cliente_id,
                fecha=datetime.strptime(request.form['fecha'], '%Y-%m-%d'),
                peso=float(request.form['peso']),
                altura=float(request.form['altura']),
                cintura=float(request.form['cintura']),
                cadera=float(request.form['cadera']),
                pecho=float(request.form['pecho']),
                brazo=float(request.form['brazo']),
                muslo=float(request.form['muslo']),
                pantorrilla=float(request.form['pantorrilla']),
                porcentaje_grasa=float(request.form['porcentaje_grasa']),
                masa_muscular=float(request.form['masa_muscular']),
                masa_grasa=float(request.form['masa_grasa']),
                notas=request.form['notas']
            )
            
            # Calcular IMC
            nueva_medicion.imc = nueva_medicion.calcular_imc()
            
            db.session.add(nueva_medicion)
            db.session.commit()
            
            flash('Medición agregada exitosamente', 'success')
            return redirect(url_for('medicion.lista_mediciones', cliente_id=cliente_id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar la medición: {str(e)}', 'danger')
    
    return render_template('medicion/agregar.html', cliente=cliente)

@medicion_bp.route('/editar/<int:medicion_id>', methods=['GET', 'POST'])
@login_required
def editar_medicion(medicion_id):
    medicion = Medicion.query.get_or_404(medicion_id)
    cliente = medicion.cliente
    
    if request.method == 'POST':
        try:
            medicion.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d')
            medicion.peso = float(request.form['peso'])
            medicion.altura = float(request.form['altura'])
            medicion.cintura = float(request.form['cintura'])
            medicion.cadera = float(request.form['cadera'])
            medicion.pecho = float(request.form['pecho'])
            medicion.brazo = float(request.form['brazo'])
            medicion.muslo = float(request.form['muslo'])
            medicion.pantorrilla = float(request.form['pantorrilla'])
            medicion.porcentaje_grasa = float(request.form['porcentaje_grasa'])
            medicion.masa_muscular = float(request.form['masa_muscular'])
            medicion.masa_grasa = float(request.form['masa_grasa'])
            medicion.notas = request.form['notas']
            
            # Recalcular IMC
            medicion.imc = medicion.calcular_imc()
            
            db.session.commit()
            flash('Medición actualizada exitosamente', 'success')
            return redirect(url_for('medicion.lista_mediciones', cliente_id=cliente.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la medición: {str(e)}', 'danger')
    
    return render_template('medicion/editar.html', medicion=medicion, cliente=cliente)

@medicion_bp.route('/eliminar/<int:medicion_id>', methods=['POST'])
@login_required
def eliminar_medicion(medicion_id):
    medicion = Medicion.query.get_or_404(medicion_id)
    cliente_id = medicion.cliente_id
    
    try:
        db.session.delete(medicion)
        db.session.commit()
        flash('Medición eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la medición: {str(e)}', 'danger')
    
    return redirect(url_for('medicion.lista_mediciones', cliente_id=cliente_id)) 