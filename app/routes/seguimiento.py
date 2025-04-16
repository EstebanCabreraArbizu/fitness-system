from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.seguimiento import Seguimiento
from app.models.meta import Meta
from app.models.cliente import Cliente
from app.models.rutina import Rutina
from app.extensions import db
from datetime import datetime
from sqlalchemy import and_

seguimiento_bp = Blueprint('seguimiento', __name__, url_prefix='/seguimiento')

@seguimiento_bp.route('/cliente/<int:cliente_id>')
@login_required
def ver_seguimiento(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    # Obtener los seguimientos a través de las rutinas del cliente
    seguimientos = Seguimiento.query\
        .join(Meta)\
        .join(Rutina)\
        .filter(Rutina.cliente_id == cliente_id)\
        .order_by(Seguimiento.fecha.desc())\
        .all()

    # Preparar datos para el gráfico: evolución de todas las metas activas
    metas_activas = []
    for rutina in cliente.rutinas:
        for meta in rutina.metas:
            if not meta.logrado:
                # Medida inicial
                datos = [{
                    'fecha': meta.fecha_registro.strftime('%Y-%m-%d'),
                    'valor': meta.medida_inicial,
                    'tipo': 'Inicial'
                }]
                # Historial de medidas
                for h in sorted(meta.historial_medidas, key=lambda x: x.fecha):
                    datos.append({
                        'fecha': h.fecha.strftime('%Y-%m-%d'),
                        'valor': h.medida,
                        'tipo': 'Historial'
                    })
                # Seguimientos
                for s in sorted(meta.seguimientos, key=lambda x: x.fecha):
                    datos.append({
                        'fecha': s.fecha.strftime('%Y-%m-%d'),
                        'valor': s.valor_actual,
                        'tipo': 'Seguimiento'
                    })
                # Eliminar duplicados por fecha (dejar el último valor de cada fecha)
                datos_dict = {}
                for d in datos:
                    datos_dict[d['fecha']] = d
                datos_final = list(datos_dict.values())
                datos_final.sort(key=lambda x: x['fecha'])
                metas_activas.append({
                    'id': meta.id,
                    'tipo_medida': meta.tipo_medida,
                    'unidad': meta.unidad,
                    'datos': datos_final
                })

    return render_template('cliente/seguimiento.html', cliente=cliente, seguimientos=seguimientos, metas_activas=metas_activas)

@seguimiento_bp.route('/agregar/<int:cliente_id>', methods=['POST'])
@login_required
def agregar_seguimiento(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    
    try:
        meta_id = request.form.get('meta_id', type=int)
        meta = Meta.query.get_or_404(meta_id)
        
        # Verificar que la meta pertenece a una rutina del cliente
        if meta.rutina.cliente_id != cliente_id:
            return jsonify({'error': 'Meta no pertenece al cliente'}), 400
        
        nuevo_seguimiento = Seguimiento(
            meta_id=meta_id,
            valor_actual=request.form.get('valor_actual', type=float),
            notas=request.form.get('notas')
        )
        
        # Actualizar el progreso de la meta
        meta.actualizar_progreso(nuevo_seguimiento.valor_actual)
        
        db.session.add(nuevo_seguimiento)
        db.session.commit()
        
        flash('Seguimiento registrado exitosamente', 'success')
        return jsonify({'success': True})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@seguimiento_bp.route('/editar/<int:seguimiento_id>', methods=['GET', 'POST'])
@login_required
def editar_seguimiento(seguimiento_id):
    seguimiento = Seguimiento.query.get_or_404(seguimiento_id)
    
    if request.method == 'POST':
        try:
            seguimiento.valor_actual = request.form.get('valor_actual', type=float)
            seguimiento.notas = request.form.get('notas')
            
            # Actualizar el progreso de la meta
            seguimiento.meta.actualizar_progreso(seguimiento.valor_actual)
            
            db.session.commit()
            flash('Seguimiento actualizado exitosamente', 'success')
            return jsonify({'success': True})
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return jsonify({
        'id': seguimiento.id,
        'valor_actual': seguimiento.valor_actual,
        'notas': seguimiento.notas
    }) 