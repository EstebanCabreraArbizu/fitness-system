import time
import re
import os
import hashlib
import traceback
from datetime import timedelta
from urllib.parse import urlparse
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.client import Client
from app.models.instructor import Instructor

users = Blueprint('users', __name__, template_folder='app/templates')

# Funciones auxiliares
def hash_password(password):
    """Genera un hash seguro para contraseñas"""
    salt = "fitsystem2025"  # En producción, usar un salt único por usuario
    return hashlib.sha256((password + salt).encode()).hexdigest()

def is_strong_password(password):
    """Verifica si la contraseña cumple con los requisitos de seguridad"""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    # Verificar requisitos: mayúscula, minúscula, número y carácter especial
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    if not re.search(r'[0-9]', password):
        return False, "La contraseña debe contener al menos un número"
    if not re.search(r'[!@#$%^&*()_\-+={}[\]|:;\'\"<>,.?/]', password):
        return False, "La contraseña debe contener al menos un carácter especial"
        
    return True, "Contraseña válida"

@users.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión de usuarios"""
    if current_user.is_authenticated:
        return redirect_based_on_role(current_user)
        
    if request.method == 'GET':
        return render_template('users/login.html')

    # Procesar formulario login
    email = request.form.get('correo', '').strip()
    password = request.form.get('contrasenia', '')
    
    if not email or not password:
        flash('Por favor ingrese correo y contraseña', 'warning')
        return redirect(url_for('users.login'))
    
    try:
        # Intentar iniciar sesión como Cliente primero
        user = authenticate_client(email, password)
        
        if not user:
            # Si no es cliente, intentar como Instructor
            user = authenticate_instructor(email, password)
            
        if user:
            # Recordar usuario por 7 días
            login_user(user, remember=True, duration=timedelta(days=7))
            flash(f'¡Bienvenido {user.get_nombre()}!', 'success')
            return redirect_based_on_role(user)
        else:
            time.sleep(0.5)  # Delay para prevenir enumeración
            flash('Usuario no encontrado o contraseña incorrecta', 'danger')
            return redirect(url_for('users.login'))
            
    except Exception as e:
        flash('Error al iniciar sesión. Por favor intente más tarde.', 'danger')
        current_app.logger.error(f"Error de login: {str(e)}")
        return redirect(url_for('users.login'))

def authenticate_client(email, password):
    """Autentica al usuario como Cliente"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Buscar usuario en tabla Cliente
        cursor.execute("""
            SELECT * FROM Cliente 
            WHERE email = %s AND status = 1
        """, (email,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            hashed_password = hash_password(password)
            stored_password = user_data['contrasenia']
            
            if hashed_password == stored_password:
                return Client(
                    id=user_data['id'],
                    nombres=user_data['nombres'],
                    apellidos=user_data['apellidos'],
                    celular=user_data['celular'],
                    email=user_data['email'],
                    contrasenia=stored_password,
                    direccion=user_data['direccion'],
                    tipo_cliente=user_data['tipo_cliente'],
                    status=user_data['status'],
                    imagen=user_data['imagen']
                )
        return None
    except Exception as e:
        current_app.logger.error(f"Error autenticando cliente: {str(e)}")
        return None

def authenticate_instructor(email, password):
    """Autentica al usuario como Instructor"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Buscar usuario en tabla Instructor
        cursor.execute("""
            SELECT * FROM Instructor 
            WHERE email = %s AND status = 1
        """, (email,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data:
            hashed_password = hash_password(password)
            stored_password = user_data['contrasenia']
            
            if hashed_password == stored_password:
                return Instructor(
                    id=user_data['id'],
                    nombres=user_data['nombres'],
                    apellidos=user_data['apellidos'],
                    celular=user_data['celular'],
                    email=user_data['email'],
                    contrasenia=stored_password,
                    status=user_data['status'],
                    imagen=user_data['imagen']
                )
        return None
    except Exception as e:
        current_app.logger.error(f"Error autenticando instructor: {str(e)}")
        return None

def redirect_based_on_role(user):
    """Redirecciona al usuario según su tipo"""
    next_url = request.args.get('next')
    
    # Validar URL next para prevenir redirecciones forzadas
    if next_url and urlparse(next_url).netloc == request.host:
        return redirect(next_url)
    
    # Redirección según tipo de usuario
    if isinstance(user, Client):
        return redirect(url_for('client.dashboard'))
    elif isinstance(user, Instructor):
        return redirect(url_for('instructor.dashboard'))
    else:
        flash('Tipo de usuario no reconocido.', 'danger')
        return redirect(url_for('users.login'))

@users.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Maneja el registro de nuevos usuarios"""
    if request.method == 'GET':
        return render_template('users/create_account.html')
        
    try:
        # Datos básicos
        nombres = request.form.get('nombre', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        email = request.form.get('correo', '').strip().lower()
        contrasenia = request.form.get('contrasenia', '')
        confirmacion = request.form.get('confirmContrasenia', '')
        
        # Datos personales
        celular = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        peso = request.form.get('peso', 0)
        altura = request.form.get('altura', 0)
        
        # Tipo de usuario
        tipo_usuario = request.form.get('tipoUsuario', '')
        tipo_cliente = request.form.get('tipo_cliente', 'regular')
        
        # Validaciones básicas
        if not nombres or not email or not contrasenia or not celular or not tipo_usuario:
            flash('Todos los campos marcados con * son obligatorios', 'warning')
            return redirect(url_for('users.add_user'))
            
        if contrasenia != confirmacion:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(url_for('users.add_user'))
            
        is_valid, password_msg = is_strong_password(contrasenia)
        if not is_valid:
            flash(password_msg, 'warning')
            return redirect(url_for('users.add_user'))
            
        # Validar email
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            flash('Por favor ingrese un correo electrónico válido', 'warning')
            return redirect(url_for('users.add_user'))
            
        # Validar teléfono
        if not celular.isdigit():
            flash('El número de teléfono solo debe contener dígitos', 'warning')
            return redirect(url_for('users.add_user'))
        
        # Procesar imagen
        imagen = process_profile_image(request)
        if isinstance(imagen, tuple):
            # Si hay error, imagen es una tupla (None, mensaje_error)
            flash(imagen[1], 'warning')
            return redirect(url_for('users.add_user'))
        
        # Verificar existencia de correo
        if email_exists(email):
            flash('Este correo electrónico ya está registrado', 'danger')
            return redirect(url_for('users.add_user'))
            
        # Hashear contraseña
        hashed_password = hash_password(contrasenia)
        
        # Crear el usuario según el tipo seleccionado
        user = create_user(tipo_usuario, nombres, apellidos, celular, email, 
                         hashed_password, direccion, tipo_cliente, imagen, peso, altura)
        
        if not user:
            flash('Tipo de usuario no válido', 'danger')
            return redirect(url_for('users.add_user'))
        
        # Iniciar sesión con el usuario creado
        login_user(user)
        
        flash(f'¡Bienvenido a FitSystem, {nombres}! Tu cuenta ha sido creada exitosamente.', 'success')
        
        # Redirigir según el tipo de usuario
        if tipo_usuario == 'Cliente':
            return redirect(url_for('client.dashboard'))
        else:
            return redirect(url_for('instructor.dashboard'))
        
    except Exception as e:
        # Registrar el error completo
        import traceback
        error_details = traceback.format_exc()
        current_app.logger.error(f"Error al registrar usuario: {str(e)}\n{error_details}")
        flash('Error al registrar usuario. Por favor intente nuevamente.', 'danger')
        return redirect(url_for('users.add_user'))

def process_profile_image(request):
    """Procesa la imagen de perfil cargada"""
    imagen_file = request.files.get('imagen')
    
    if not imagen_file or not imagen_file.filename:
        return 'default-user.png'
        
    filename = secure_filename(imagen_file.filename)
    
    # Añadir timestamp para evitar colisiones
    name_parts = os.path.splitext(filename)
    unique_filename = f"{name_parts[0]}_{int(time.time())}{name_parts[1]}"
    
    # Verificar tipo de archivo
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    if '.' in unique_filename and unique_filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        img_path = os.path.join('app/static/img', unique_filename)
        imagen_file.save(img_path)
        
        # Optimizar imagen
        try:
            from PIL import Image
            img = Image.open(img_path)
            # Redimensionar si es demasiado grande
            if img.width > 800 or img.height > 800:
                img.thumbnail((800, 800), Image.LANCZOS)
            # Guardar con compresión
            img.save(img_path, optimize=True, quality=85)
        except ImportError:
            current_app.logger.warning("PIL no disponible, no se puede optimizar la imagen")
        
        return unique_filename
    else:
        return None, 'Formato de imagen no permitido. Use: png, jpg, jpeg, gif, webp'

def email_exists(email):
    """Verifica si el correo ya está registrado en cualquier tabla de usuarios"""
    conn = None
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verificar en tabla Cliente
        cursor.execute("SELECT email FROM Cliente WHERE email = %s", (email,))
        if cursor.fetchone():
            return True
            
        # Verificar en tabla Instructor
        cursor.execute("SELECT email FROM Instructor WHERE email = %s", (email,))
        if cursor.fetchone():
            return True
            
        return False
    finally:
        if cursor:
            cursor.close()

def create_user(tipo_usuario, nombres, apellidos, celular, email, 
                contrasenia, direccion, tipo_cliente, imagen, peso, altura):
    """Crea un nuevo usuario en la base de datos"""
    conn = None
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        if tipo_usuario == 'Cliente':
            # Convertir peso y altura a valores numéricos
            try:
                peso = float(peso) if peso else 0
                altura = float(altura) if altura else 0
            except ValueError:
                peso = 0
                altura = 0
            
            # Insertar en la tabla Cliente
            cursor.execute("""
                INSERT INTO Cliente (nombres, apellidos, celular, email, contrasenia, 
                                    direccion, tipo_cliente, status, imagen, peso, altura) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (nombres, apellidos, celular, email, contrasenia, 
                  direccion, tipo_cliente, 1, imagen, peso, altura))
            
            conn.commit()
            new_user_id = cursor.lastrowid
            
            # Crear el objeto Cliente para login
            return Client(
                id=new_user_id,
                nombres=nombres,
                apellidos=apellidos,
                celular=celular,
                email=email,
                contrasenia=contrasenia,
                direccion=direccion,
                tipo_cliente=tipo_cliente,
                status=1,
                imagen=imagen
            )
            
        elif tipo_usuario == 'Instructor':
            # Insertar en la tabla Instructor
            cursor.execute("""
                INSERT INTO Instructor (nombres, apellidos, celular, email, contrasenia, 
                                       status, imagen) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (nombres, apellidos, celular, email, contrasenia, 1, imagen))
            
            conn.commit()
            new_user_id = cursor.lastrowid
            
            # Crear el objeto Instructor para login
            return Instructor(
                id=new_user_id,
                nombres=nombres,
                apellidos=apellidos,
                celular=celular,
                email=email,
                contrasenia=contrasenia,
                status=1,
                imagen=imagen
            )
        
        return None
    except Exception as e:
        if conn:
            conn.rollback()
        current_app.logger.error(f"Error creando usuario: {str(e)}")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@users.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    """Ver y editar perfil de usuario"""
    try:
        # Determinar el tipo de usuario actual
        if isinstance(current_user, Client):
            user_type = "Cliente"
            user_table = "Cliente"
            id_field = "id"
        elif isinstance(current_user, Instructor):
            user_type = "Instructor"
            user_table = "Instructor"
            id_field = "id"
        else:
            flash('Tipo de usuario no reconocido', 'danger')
            return redirect(url_for('users.login'))
        
        # Verificar que el usuario esté accediendo a su propio perfil
        if int(current_user.get_id()) != user_id:
            flash('No tienes permiso para acceder a este perfil', 'danger')
            return redirect(url_for('client.dashboard' if isinstance(current_user, Client) else 'instructor.dashboard'))
        
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener datos del perfil
        cursor.execute(f"SELECT * FROM {user_table} WHERE {id_field} = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if request.method == 'GET':
            return render_template('users/profile.html', user=user_data, user_type=user_type)
        
        # Actualizar perfil
        nombres = request.form.get('nombre', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        celular = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        
        # Procesar cambios específicos de tipo de usuario
        if user_type == "Cliente":
            peso = request.form.get('peso', 0)
            altura = request.form.get('altura', 0)
            
            # Convertir peso y altura a valores numéricos
            try:
                peso = float(peso) if peso else 0
                altura = float(altura) if altura else 0
            except ValueError:
                peso = 0
                altura = 0
        
        # Procesar imagen
        imagen = user_data['imagen']  # Valor predeterminado
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename:
            new_imagen = process_profile_image(request)
            if isinstance(new_imagen, tuple):
                flash(new_imagen[1], 'warning')
            else:
                imagen = new_imagen
        
        # Actualizar datos según tipo de usuario
        cursor = conn.cursor()
        
        if user_type == "Cliente":
            cursor.execute("""
                UPDATE Cliente SET 
                    nombres = %s, apellidos = %s, celular = %s, direccion = %s, 
                    imagen = %s, peso = %s, altura = %s
                WHERE id = %s
            """, (nombres, apellidos, celular, direccion, imagen, peso, altura, user_id))
        else:  # Instructor
            cursor.execute("""
                UPDATE Instructor SET 
                    nombres = %s, apellidos = %s, celular = %s, imagen = %s
                WHERE id = %s
            """, (nombres, apellidos, celular, imagen, user_id))
        
        conn.commit()
        cursor.close()
        
        flash('Perfil actualizado correctamente', 'success')
        return redirect(url_for('users.profile', user_id=user_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al actualizar perfil: {str(e)}")
        flash(f'Error al actualizar perfil: {str(e)}', 'danger')
        return redirect(url_for('users.profile', user_id=user_id))

@users.route('/change_password/<int:user_id>', methods=['POST'])
@login_required
def change_password(user_id):
    """Cambiar contraseña del usuario"""
    try:
        # Verificar que el usuario esté cambiando su propia contraseña
        if int(current_user.get_id()) != user_id:
            flash('No tienes permiso para cambiar esta contraseña', 'danger')
            return redirect(url_for('users.profile', user_id=current_user.get_id()))
        
        # Determinar tabla según tipo de usuario
        if isinstance(current_user, Client):
            user_table = "Cliente"
            id_field = "id"
        elif isinstance(current_user, Instructor):
            user_table = "Instructor"
            id_field = "id"
        else:
            flash('Tipo de usuario no reconocido', 'danger')
            return redirect(url_for('users.login'))
        
        # Obtener datos del formulario
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        # Validaciones
        if not current_password or not new_password:
            flash('Todos los campos son obligatorios', 'warning')
            return redirect(url_for('users.profile', user_id=user_id))
        
        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden', 'warning')
            return redirect(url_for('users.profile', user_id=user_id))
        
        # Verificar contraseña actual
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT contrasenia FROM {user_table} WHERE {id_field} = %s", (user_id,))
        user_data = cursor.fetchone()
        
        if not user_data or hash_password(current_password) != user_data['contrasenia']:
            flash('La contraseña actual es incorrecta', 'danger')
            return redirect(url_for('users.profile', user_id=user_id))
        
        # Validar nueva contraseña
        is_valid, password_msg = is_strong_password(new_password)
        if not is_valid:
            flash(password_msg, 'warning')
            return redirect(url_for('users.profile', user_id=user_id))
        
        # Actualizar contraseña
        hashed_new_password = hash_password(new_password)
        cursor.execute(
            f"UPDATE {user_table} SET contrasenia = %s WHERE {id_field} = %s", 
            (hashed_new_password, user_id)
        )
        
        conn.commit()
        cursor.close()
        
        flash('Contraseña actualizada exitosamente', 'success')
        return redirect(url_for('users.profile', user_id=user_id))
        
    except Exception as e:
        current_app.logger.error(f"Error al cambiar contraseña: {str(e)}")
        flash(f'Error al cambiar contraseña: {str(e)}', 'danger')
        return redirect(url_for('users.profile', user_id=user_id))

@users.route('/logout')
@login_required
def logout():
    """Cierra la sesión del usuario"""
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('users.login'))