from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.cliente import Cliente
from app.models.discipline import Discipline
from app.models.instructor import Instructor
from app.models.associations import discipline_instructor
from app import db
from werkzeug.utils import secure_filename
import os
from flask_login import login_required

client_bp = Blueprint('client', __name__, url_prefix='/clients')

# Función auxiliar para manejar la subida de imágenes
def save_image(file):
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Obtener la ruta absoluta del directorio uploads
        uploads_dir = os.path.join(current_app.root_path, 'static', 'uploads')
        
        # Crear el directorio si no existe
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        
        # Guardar el archivo
        file_path = os.path.join(uploads_dir, filename)
        file.save(file_path)
        return filename
    return 'default.png'

@client_bp.route('/')
@login_required
def index():
    clientes = Cliente.query.all()
    return render_template('client/index.html', clientes=clientes)

@client_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario con valores por defecto
            data = {
                'nombres': request.form.get('nombres', ''),
                'apellidos': request.form.get('apellidos', ''),
                'celular': request.form.get('celular', ''),
                'email': request.form.get('email', ''),
                'direccion': request.form.get('direccion', ''),
                'tipo_cliente': request.form.get('tipo_cliente', 'externo'),
                'contrasenia': '12345678'  # Contraseña por defecto
            }

            # Validar datos requeridos
            if not all([data['nombres'], data['apellidos'], data['email']]):
                flash('Por favor complete todos los campos requeridos', 'danger')
                return redirect(url_for('client.create'))

            # Crear nuevo cliente
            cliente = Cliente(
                nombres=data['nombres'],
                apellidos=data['apellidos'],
                celular=data['celular'],
                email=data['email'],
                contrasenia=data['contrasenia'],
                direccion=data['direccion'],
                tipo_cliente=data['tipo_cliente'],
                status=1,
                imagen='default.png'  # Imagen por defecto
            )
            
            # Manejar la imagen
            if 'imagen' in request.files:
                file = request.files['imagen']
                filename = save_image(file)
                if filename:
                    cliente.imagen = filename

            # Manejar disciplinas
            discipline_ids = request.form.getlist('disciplines[]')
            if discipline_ids:
                disciplines = Discipline.query.filter(Discipline.id.in_(discipline_ids)).all()
                cliente.disciplines.extend(disciplines)

            # Manejar instructores
            instructor_ids = request.form.getlist('instructors[]')
            if instructor_ids:
                instructors = Instructor.query.filter(Instructor.id.in_(instructor_ids)).all()
                cliente.instructors = instructors

            # Guardar en la base de datos
            db.session.add(cliente)
            db.session.commit()
            flash('Cliente creado exitosamente', 'success')
            return redirect(url_for('client.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el cliente: {str(e)}', 'danger')
            return redirect(url_for('client.create'))

    # GET request
    disciplines = Discipline.query.all()
    instructors = Instructor.query.all()
    
    # Falta crear el diccionario instructors_by_discipline
    instructors_by_discipline = {}
    for instructor in instructors:
        for discipline in instructor.disciplines:
            if discipline.id not in instructors_by_discipline:
                instructors_by_discipline[discipline.id] = []
            instructors_by_discipline[discipline.id].append(instructor)
    
    return render_template('client/create.html',
                         disciplines=disciplines,
                         instructors=instructors,
                         instructors_by_discipline=instructors_by_discipline)

@client_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cliente = Cliente.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            cliente.nombres = request.form.get('nombres', cliente.nombres)
            cliente.apellidos = request.form.get('apellidos', cliente.apellidos)
            cliente.celular = request.form.get('celular', cliente.celular)
            cliente.email = request.form.get('email', cliente.email)
            cliente.direccion = request.form.get('direccion', cliente.direccion)
            cliente.tipo_cliente = request.form.get('tipo_cliente', cliente.tipo_cliente)

            # Manejar la imagen
            if 'imagen' in request.files:
                file = request.files['imagen']
                filename = save_image(file)
                if filename:
                    cliente.imagen = filename

            # Actualizar disciplinas
            discipline_ids = request.form.getlist('disciplines[]')
            if discipline_ids:
                cliente.disciplines = Discipline.query.filter(Discipline.id.in_(discipline_ids)).all()

            # Actualizar instructores
            instructor_ids = request.form.getlist('instructors[]')
            if instructor_ids:
                cliente.instructors = Instructor.query.filter(Instructor.id.in_(instructor_ids)).all()

            db.session.commit()
            flash('Cliente actualizado exitosamente', 'success')
            return redirect(url_for('client.index'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el cliente: {str(e)}', 'danger')

    disciplines = Discipline.query.all()
    instructors = Instructor.query.all()
    return render_template('client/edit.html', 
                         cliente=cliente,
                         disciplines=disciplines,
                         instructors=instructors)

@client_bp.route('/delete/<int:id>')
def delete(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el cliente', 'danger')
    return redirect(url_for('client.index'))
