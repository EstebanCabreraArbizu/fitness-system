from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.rutina import Rutina, EjercicioRutina
from app.models.cliente import Cliente
from app.models.instructor import Instructor
from app.models.discipline import Discipline
from app import db
from datetime import datetime
from flask_login import login_required, current_user

rutina_bp = Blueprint('rutina', __name__, url_prefix='/rutinas')

@rutina_bp.route('/lista/<int:cliente_id>')
@login_required
def lista_rutinas(cliente_id):
    cliente = Cliente.query.get_or_404(cliente_id)
    rutinas = Rutina.query.filter_by(cliente_id=cliente_id).all()
    
    # Precarga los ejercicios para cada rutina
    for rutina in rutinas:
        # Cargar ejercicios ordenados por día y orden
        ejercicios = EjercicioRutina.query.filter_by(rutina_id=rutina.id)\
            .order_by(EjercicioRutina.dia_semana, EjercicioRutina.orden).all()
        
        # Agrupar ejercicios por día
        ejercicios_por_dia = {}
        for ejercicio in ejercicios:
            if ejercicio.dia_semana not in ejercicios_por_dia:
                ejercicios_por_dia[ejercicio.dia_semana] = []
            ejercicios_por_dia[ejercicio.dia_semana].append(ejercicio)
        
        rutina.ejercicios_por_dia = ejercicios_por_dia
    
    return render_template('rutina/lista.html', 
                         rutinas=rutinas, 
                         cliente=cliente)

@rutina_bp.route('/crear/<int:cliente_id>', methods=['GET', 'POST'])
@login_required
def crear(cliente_id):
    disciplines = Discipline.query.all()
    
    if request.method == 'POST':
        try:
            # Crear nueva rutina
            nueva_rutina = Rutina(
                cliente_id=cliente_id,
                instructor_id=current_user.id,
                discipline_id=request.form['discipline_id'],
                titulo=request.form['titulo'],
                descripcion=request.form['descripcion'],
                fecha_inicio=request.form['fecha_inicio'],
                fecha_fin=request.form['fecha_fin'],
                nivel=request.form['nivel'],
                status=1
            )
            db.session.add(nueva_rutina)
            db.session.flush()  # Para obtener el ID de la rutina

            # Crear ejercicios
            nombres = request.form.getlist('nombres[]')
            series = request.form.getlist('series[]')
            repeticiones = request.form.getlist('repeticiones[]')
            descansos = request.form.getlist('descansos[]')
            ordenes = request.form.getlist('ordenes[]')
            notas = request.form.getlist('notas[]')

            for i in range(len(nombres)):
                # Obtener los días seleccionados para este ejercicio
                dias = []
                for dia in range(1, 8):
                    if request.form.get(f'dias[{i}][{dia}]'):
                        dias.append(dia)
                
                # Crear un ejercicio por cada día seleccionado
                for dia in dias:
                    ejercicio = EjercicioRutina(
                        rutina_id=nueva_rutina.id,
                        nombre=nombres[i],
                        series=series[i],
                        repeticiones=repeticiones[i],
                        descanso=descansos[i],
                        dia_semana=dia,
                        orden=ordenes[i],
                        notas=notas[i]
                    )
                    db.session.add(ejercicio)

            db.session.commit()
            flash('Rutina creada exitosamente', 'success')
            return redirect(url_for('rutina.lista_rutinas', cliente_id=cliente_id))
        
        except Exception as e:
            db.session.rollback()
            flash('Error al crear la rutina: ' + str(e), 'error')

    return render_template('rutina/crear.html', 
                         cliente_id=cliente_id,
                         disciplines=disciplines)

@rutina_bp.route('/editar/<int:rutina_id>', methods=['GET', 'POST'])
@login_required
def editar(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)
    cliente = Cliente.query.get_or_404(rutina.cliente_id)
    # Agrupamos los ejercicios por nombre para manejar los días múltiples
    ejercicios_agrupados = {}
    for ejercicio in EjercicioRutina.query.filter_by(rutina_id=rutina_id).order_by(EjercicioRutina.orden).all():
        if ejercicio.nombre not in ejercicios_agrupados:
            ejercicios_agrupados[ejercicio.nombre] = {
                'nombre': ejercicio.nombre,
                'series': ejercicio.series,
                'repeticiones': ejercicio.repeticiones,
                'descanso': ejercicio.descanso,
                'orden': ejercicio.orden,
                'notas': ejercicio.notas,
                'dias': []
            }
        ejercicios_agrupados[ejercicio.nombre]['dias'].append(ejercicio.dia_semana)
    
    disciplines = Discipline.query.all()

    if request.method == 'POST':
        rutina.discipline_id = request.form['discipline_id']
        rutina.titulo = request.form['titulo']
        rutina.descripcion = request.form['descripcion']
        rutina.fecha_inicio = datetime.strptime(request.form['fecha_inicio'], '%Y-%m-%d')
        rutina.fecha_fin = datetime.strptime(request.form['fecha_fin'], '%Y-%m-%d')
        rutina.nivel = request.form['nivel']
        
        # Eliminar ejercicios anteriores
        EjercicioRutina.query.filter_by(rutina_id=rutina.id).delete()
        
        # Agregar nuevos ejercicios
        nombres = request.form.getlist('nombres[]')
        series = request.form.getlist('series[]')
        repeticiones = request.form.getlist('repeticiones[]')
        descansos = request.form.getlist('descansos[]')
        ordenes = request.form.getlist('ordenes[]')
        notas = request.form.getlist('notas[]')
        
        for i in range(len(nombres)):
            # Obtener los días seleccionados para este ejercicio
            dias = []
            for dia in range(1, 8):
                if request.form.get(f'dias[{i}][{dia}]'):
                    dias.append(dia)
            
            # Crear un ejercicio por cada día seleccionado
            for dia in dias:
                ejercicio = EjercicioRutina(
                    rutina_id=rutina.id,
                    nombre=nombres[i],
                    series=series[i],
                    repeticiones=repeticiones[i],
                    descanso=descansos[i],
                    dia_semana=dia,
                    orden=ordenes[i],
                    notas=notas[i]
                )
                db.session.add(ejercicio)
        
        db.session.commit()
        flash('Rutina actualizada exitosamente', 'success')
        return redirect(url_for('rutina.lista_rutinas', cliente_id=rutina.cliente_id))
    
    return render_template('rutina/editar.html',
                         rutina=rutina,
                         ejercicios=list(ejercicios_agrupados.values()),
                         disciplines=disciplines,
                         cliente=cliente)

@rutina_bp.route('/eliminar/<int:rutina_id>')
def eliminar(rutina_id):
    rutina = Rutina.query.get_or_404(rutina_id)
    cliente_id = rutina.cliente_id
    
    try:
        db.session.delete(rutina)
        db.session.commit()
        flash('Rutina eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la rutina', 'danger')
    
    return redirect(url_for('rutina.lista_rutinas', cliente_id=cliente_id)) 