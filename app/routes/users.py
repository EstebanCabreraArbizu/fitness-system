import re
import os
import hashlib
import time
from datetime import timedelta
from urllib.parse import urlparse
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.user import User

users = Blueprint('users', __name__, template_folder='app/templates')

# Funciones auxiliares
def hash_password(password):
    """Devuelve la contraseña sin hashear (para desarrollo)"""
    return password


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
        return redirect(url_for('dieta.index'))

    if request.method == 'GET':
        return render_template('users/login.html')

    # Procesar formulario login
    email = request.form.get('correo', '').strip()
    password = request.form.get('contrasenia', '')

    if not email or not password:
        flash('Por favor ingrese correo y contraseña', 'warning')
        return render_template('users/login.html')

    try:
        # Obtener el usuario primero para verificar que existe
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verificar si el usuario existe
        cursor.execute("""
            SELECT id, email, contrasenia, Tipo_usuario_id, status FROM Usuario WHERE email = %s
        """, (email,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            current_app.logger.warning(f"Intento de login con usuario inexistente: {email}")
            time.sleep(0.5)  # Delay para prevenir enumeración
            flash('Usuario no encontrado o cuenta desactivada', 'danger')
            return render_template('users/login.html')
        
        if user_data['status'] != 1:
            current_app.logger.warning(f"Intento de login con cuenta desactivada: {email}")
            time.sleep(0.5)
            flash('Esta cuenta está desactivada', 'danger')
            return render_template('users/login.html')
            
        # Verificar contraseña
        hashed_password = hash_password(password)
        if hashed_password != user_data['contrasenia']:
            current_app.logger.warning(f"Intento de login con contraseña incorrecta: {email}")
            time.sleep(0.5)  # Delay para prevenir ataques
            flash('Contraseña incorrecta', 'danger')
            return render_template('users/login.html')
        
        # Registrar datos básicos del usuario que intenta iniciar sesión    
        current_app.logger.info(f"Login exitoso para usuario: {email} (ID: {user_data['id']}, Tipo: {user_data['Tipo_usuario_id']})")
        
        # Si llegamos aquí, la autenticación es correcta, usamos la función completa para cargar todos los datos
        try:
            user = authenticate_user(email, password)
            
            if user:
                login_user(user, remember=True, duration=timedelta(days=7))
                flash(f'¡Bienvenido {user.get_nombre()}!', 'success')
                return redirect_based_on_role(user)
            else:
                # Este caso no debería ocurrir normalmente
                current_app.logger.error(f"Error cargando datos completos del usuario: {email}. Usuario existe pero authenticate_user devolvió None")
                flash('Error al cargar datos de usuario. Por favor intente más tarde.', 'danger')
                return render_template('users/login.html')
                
        except Exception as auth_error:
            current_app.logger.error(f"Error en authenticate_user para {email}: {str(auth_error)}")
            flash('Error al procesar datos de usuario. Por favor intente más tarde.', 'danger')
            return render_template('users/login.html')

    except Exception as e:
        current_app.logger.error(f"Error general de login: {str(e)}")
        flash('Error al iniciar sesión. Por favor intente más tarde.', 'danger')
        return render_template('users/login.html')

def authenticate_user(email, password):
    """Autentica al usuario usando la tabla unificada"""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()

        # Buscar usuario en tabla Usuario con datos específicos del tipo
        cursor.execute("""
            SELECT u.*,
                IFNULL((SELECT direccion FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as direccion,
                IFNULL((SELECT tipo_cliente FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as tipo_cliente,
                IFNULL((SELECT nivel_actividad FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as nivel_actividad,
                IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as peso,
                IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as altura,
                IFNULL((SELECT certificaciones FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as certificaciones,
                IFNULL((SELECT especialidad FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as especialidad,
                IFNULL((SELECT fecha_pago FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as fecha_pago
            FROM Usuario u
            WHERE u.email = %s AND u.status = 1
        """, (email,))

        user_data = cursor.fetchone()
        cursor.close()

        if user_data:
            hashed_password = hash_password(password)
            stored_password = user_data['contrasenia']

            if hashed_password == stored_password:
                return User(
                    id=user_data['id'],
                    nombres=user_data['nombres'],
                    apellidos=user_data['apellidos'],
                    celular=user_data['celular'],
                    email=user_data['email'],
                    contrasenia=stored_password,
                    status=user_data['status'],
                    imagen=user_data['imagen'],
                    tipo_usuario_id=user_data['Tipo_usuario_id'],
                    direccion=user_data['direccion'],
                    tipo_cliente=user_data['tipo_cliente'],
                    nivel_actividad=user_data['nivel_actividad'],
                    peso=user_data['peso'],
                    altura=user_data['altura'],
                    fecha_registro=user_data['fecha_registro'],
                    fecha_pago=user_data.get('fecha_pago'),
                    certificaciones=user_data['certificaciones'],
                    especialidad=user_data['especialidad']
                )
        return None
    except Exception as e:
        current_app.logger.error(f"Error autenticando usuario: {str(e)}")
        return None

def redirect_based_on_role(user):
    """Redirecciona al usuario según su tipo"""
    if not user.is_authenticated:
        flash('Debes iniciar sesión para acceder a esta página.', 'warning')
        return redirect(url_for('users.login'))
    
    next_url = request.args.get('next')

    # Validar URL next para prevenir redirecciones forzadas
    if next_url and (urlparse(next_url).netloc == request.host or urlparse(next_url).netloc == ''):
        return redirect(next_url)

    # Redirección según tipo de usuario
    if user.is_client():
        return redirect(url_for('dieta.index'))
    elif user.is_instructor():
        return redirect(url_for('alumnos.index'))
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
        nivel_actividad = request.form.get('nivel_actividad', '').strip()

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
                           hashed_password, direccion, tipo_cliente, imagen, nivel_actividad)

        if not user:
            flash('Tipo de usuario no válido', 'danger')
            return redirect(url_for('users.add_user'))

        # Iniciar sesión con el usuario creado
        login_user(user)

        flash(
            f'¡Bienvenido a FitSystem, {nombres}! Tu cuenta ha sido creada exitosamente.', 'success')

        # Redirigir según el tipo de usuario
        if tipo_usuario == 'Cliente':
            return redirect(url_for('client.dashboard'))
        else:
            return redirect(url_for('instructor.dashboard'))

    except Exception as e:
        # Registrar el error completo
        import traceback
        error_details = traceback.format_exc()
        current_app.logger.error(
            f"Error al registrar usuario: {str(e)}\n{error_details}")
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
            current_app.logger.warning(
                "PIL no disponible, no se puede optimizar la imagen")

        return unique_filename
    else:
        return None, 'Formato de imagen no permitido. Use: png, jpg, jpeg, gif, webp'


def email_exists(email):
    """Verifica si el correo ya está registrado en cualquier tabla de usuarios"""
    conn = get_db(current_app)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Usuario WHERE email = %s", (email,))
    return True if cursor.fetchone() else False


def create_user(tipo_usuario, nombres, apellidos, celular, email,
                contrasenia, direccion, tipo_cliente, imagen, nivel_actividad):
    """Crea un nuevo usuario en la base de datos"""
    conn = None
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()

        # Insertar en tabla Usuario unificada
        cursor.execute("""
            INSERT INTO Usuario (
                nombres, apellidos, celular, email, contrasenia, 
                status, imagen, fecha_registro, Tipo_usuario_id
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, NOW(), %s
            )
        """, (
            nombres, apellidos, celular, email, contrasenia,
            1, imagen, 1 if tipo_usuario == 'Cliente' else 2
        ))
        
        user_id = cursor.lastrowid
        
        # Si es cliente, insertar datos adicionales en tabla Cliente_datos
        if tipo_usuario == 'Cliente':
            cursor.execute("""
                INSERT INTO Cliente_datos (
                    Usuario_id, direccion, tipo_cliente, nivel_actividad
                ) VALUES (%s, %s, %s, %s)
            """, (
                user_id, direccion, tipo_cliente, nivel_actividad
            ))

        conn.commit()
        
        # Obtener el usuario recién creado
        return User.get_by_id(user_id)
    except Exception as e:
        if conn:
            conn.rollback()
        current_app.logger.error(f"Error al crear usuario: {str(e)}")
        return None
    finally:
        if cursor:
            cursor.close()


@users.route('/profile/<int:user_id>', methods=['GET', 'POST'])
@login_required
def profile(user_id):
    """Ver y editar perfil de usuario"""
    try:
        # Verificar acceso al propio perfil
        if f"u_{user_id}" != current_user.get_id():
            flash('No tienes permiso para acceder a este perfil', 'danger')
            return redirect(url_for('dieta.index'))

        conn = get_db(current_app)
        cursor = conn.cursor()

        # Obtener datos del perfil de usuario unificado con LIMIT 1 en todas las subconsultas
        cursor.execute("""
            SELECT u.*,
                IFNULL((SELECT direccion FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as direccion,
                IFNULL((SELECT nivel_actividad FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as nivel_actividad,
                IFNULL((SELECT tipo_cliente FROM Cliente_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as tipo_cliente,
                IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as peso,
                IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as altura,
                IFNULL((SELECT certificaciones FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as certificaciones,
                IFNULL((SELECT especialidad FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as especialidad,
                IFNULL((SELECT estudios FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as estudios,
                IFNULL((SELECT anios_experiencia FROM Instructor_datos WHERE Usuario_id = u.id LIMIT 1), NULL) as anios_experiencia
            FROM Usuario u
            WHERE u.id = %s
        """, (user_id,))
        
        user_data = cursor.fetchone()
        cursor.close()
        
        if not user_data:
            flash('Usuario no encontrado', 'danger')
            return redirect(url_for('dieta.index'))
            
        user_type = "Instructor" if user_data['Tipo_usuario_id'] == 2 else "Cliente"

        if request.method == 'GET':
            return render_template('users/profile.html', user=user_data, user_type=user_type)

        # Actualizar perfil
        nombres = request.form.get('nombre', '').strip()
        apellidos = request.form.get('apellidos', '').strip()
        celular = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        
        # Validar datos
        if not nombres or not apellidos or not celular:
            flash('Los campos marcados con * son obligatorios', 'warning')
            return render_template('users/profile.html', user=user_data, user_type=user_type)
        
        # Procesar imagen
        imagen = user_data['imagen']  # Valor predeterminado
        imagen_file = request.files.get('imagen')
        if imagen_file and imagen_file.filename:
            new_imagen = process_profile_image(request)
            if isinstance(new_imagen, tuple):
                flash(new_imagen[1], 'warning')
            else:
                imagen = new_imagen

        # Iniciar transacción
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Actualizar datos básicos en tabla Usuario
            cursor.execute("""
                UPDATE Usuario SET
                    nombres = %s, apellidos = %s, celular = %s, imagen = %s
                WHERE id = %s
            """, (nombres, apellidos, celular, imagen, user_id))

            # Actualizar datos específicos según tipo de usuario
            if user_type == "Cliente":
                peso = request.form.get('peso', 0)
                altura = request.form.get('altura', 0)
                tipo_cliente = request.form.get('tipo_cliente', 'regular')
                nivel_actividad = request.form.get('nivel_actividad', 'intermedio')
                
                # Convertir peso y altura a valores numéricos
                try:
                    peso = float(peso) if peso else 0
                    altura = float(altura) if altura else 0
                except ValueError:
                    peso = 0
                    altura = 0
                    
                # Verificar si ya existe registro en Cliente_datos
                cursor.execute("SELECT id FROM Cliente_datos WHERE Usuario_id = %s LIMIT 1", (user_id,))
                cliente_datos = cursor.fetchone()
                
                if cliente_datos:
                    # Actualizar registro existente
                    cursor.execute("""
                        UPDATE Cliente_datos SET
                            direccion = %s, tipo_cliente = %s, nivel_actividad = %s
                        WHERE Usuario_id = %s
                    """, (direccion, tipo_cliente, nivel_actividad, user_id))
                else:
                    # Crear nuevo registro
                    cursor.execute("""
                        INSERT INTO Cliente_datos (Usuario_id, direccion, tipo_cliente, nivel_actividad)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, direccion, tipo_cliente, nivel_actividad))
                
                # Registrar nuevas medidas si cambian
                if (peso != user_data.get('peso', 0) or altura != user_data.get('altura', 0)) and (peso > 0 and altura > 0):
                    imc = round(peso / ((altura / 100) ** 2), 2)
                    cursor.execute("""
                        INSERT INTO Historial_Medidas (Usuario_id, peso, altura, imc)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, peso, altura, imc))
                    
            elif user_type == "Instructor":
                certificaciones = request.form.get('certificaciones', '')
                especialidad = request.form.get('especialidad', '')
                estudios = request.form.get('estudios', '')
                
                # Validar anios_experiencia
                try:
                    anios_experiencia = int(request.form.get('anios_experiencia', 0))
                    if anios_experiencia < 0:
                        anios_experiencia = 0
                except ValueError:
                    anios_experiencia = 0
                
                # Verificar si ya existe registro en Instructor_datos
                cursor.execute("SELECT id FROM Instructor_datos WHERE Usuario_id = %s LIMIT 1", (user_id,))
                instructor_datos = cursor.fetchone()
                
                if instructor_datos:
                    # Actualizar registro existente
                    cursor.execute("""
                        UPDATE Instructor_datos SET
                            certificaciones = %s, especialidad = %s, anios_experiencia = %s, estudios = %s
                        WHERE Usuario_id = %s
                    """, (certificaciones, especialidad, anios_experiencia, estudios, user_id))
                else:
                    # Crear nuevo registro
                    cursor.execute("""
                        INSERT INTO Instructor_datos (Usuario_id, certificaciones, especialidad, anios_experiencia, estudios)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (user_id, certificaciones, especialidad, anios_experiencia, estudios))

            conn.commit()
            
            # Actualizar el objeto usuario en la sesión actual
            if current_user.id == user_id:
                current_user.nombres = nombres
                current_user.apellidos = apellidos
                current_user.celular = celular
                current_user.imagen = imagen
                if user_type == "Cliente":
                    current_user.direccion = direccion
                    current_user.tipo_cliente = tipo_cliente
                    current_user.nivel_actividad = nivel_actividad
                    if peso > 0:
                        current_user.peso = peso
                    if altura > 0:
                        current_user.altura = altura
                elif user_type == "Instructor":
                    current_user.certificaciones = certificaciones
                    current_user.especialidad = especialidad
            
            flash('Perfil actualizado correctamente', 'success')
            return redirect(url_for('users.profile', user_id=user_id))
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

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
        if current_user.is_client() or current_user.is_instructor():
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

        cursor.execute(
            f"SELECT contrasenia FROM Usuario WHERE {id_field} = %s", (user_id,))
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
            f"UPDATE Usuario SET contrasenia = %s WHERE {id_field} = %s",
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

@users.route('/instructor_profile', methods=['GET'])
@login_required
def instructor_profile():
    """Vista detallada del perfil del instructor"""
    if not current_user.is_instructor():
        flash('Esta página es solo para instructores', 'warning')
        return redirect(url_for('dieta.index'))
    
    try:
        user_id = current_user.id
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Obtener datos del instructor
        cursor.execute("""
            SELECT u.*,
                   id.certificaciones, id.estudios, id.anios_experiencia, id.especialidad
            FROM Usuario u
            LEFT JOIN Instructor_datos id ON u.id = id.Usuario_id
            WHERE u.id = %s
        """, (user_id,))
        
        instructor_data = cursor.fetchone()
        
        # Obtener disciplinas del instructor
        cursor.execute("""
            SELECT d.*
            FROM Discipline d
            JOIN Discipline_Instructor di ON d.id = di.Discipline_id
            WHERE di.Usuario_id = %s
        """, (user_id,))
        
        disciplinas = cursor.fetchall()
        
        # Obtener alumnos asignados
        cursor.execute("""
            SELECT u.*, 
                   cd.nivel_actividad, cd.tipo_cliente,
                   (SELECT COUNT(*) FROM Rutina WHERE Usuario_id = u.id) as num_rutinas,
                   (SELECT COUNT(*) FROM Dieta WHERE Usuario_id = u.id) as num_dietas
            FROM Usuario u
            JOIN Cliente_datos cd ON u.id = cd.Usuario_id
            JOIN Cliente_Instructor ci ON u.id = ci.Usuario_id
            WHERE ci.Usuario_2_id = %s
            LIMIT 10
        """, (user_id,))
        
        alumnos = cursor.fetchall()
        
        # Obtener productos del instructor
        cursor.execute("""
            SELECT p.*,
                   (SELECT image_name FROM Product_images WHERE Product_id = p.id LIMIT 1) as imagen
            FROM Product p
            JOIN Instructor_Products ip ON p.id = ip.Product_id
            WHERE ip.Usuario_id = %s
            LIMIT 6
        """, (user_id,))
        
        productos = cursor.fetchall()
        
        # Obtener servicios del instructor
        cursor.execute("""
            SELECT s.*, 
                   COUNT(DISTINCT sh.id) as total_horarios
            FROM Servicio s
            LEFT JOIN Servicio_Horario sh ON s.id = sh.servicio_id
            WHERE s.instructor_id = %s
            GROUP BY s.id
            ORDER BY s.fecha_creacion DESC
            LIMIT 6
        """, (user_id,))
        
        servicios = cursor.fetchall()
        
        # Contar estadísticas
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM Cliente_Instructor WHERE Usuario_2_id = %s) as total_alumnos,
                (SELECT COUNT(*) FROM Rutina r JOIN Cliente_Instructor ci ON r.Usuario_id = ci.Usuario_id WHERE ci.Usuario_2_id = %s) as total_rutinas,
                (SELECT COUNT(*) FROM Dieta d WHERE d.Usuario_2_id = %s) as total_dietas,
                (SELECT COUNT(*) FROM Instructor_Products WHERE Usuario_id = %s) as total_productos,
                (SELECT COUNT(*) FROM Servicio WHERE instructor_id = %s) as total_servicios
        """, (user_id, user_id, user_id, user_id, user_id))
        
        stats = cursor.fetchone()
        
        cursor.close()
        
        return render_template('users/instructor_profile.html', 
                              instructor=instructor_data,
                              disciplinas=disciplinas,
                              alumnos=alumnos,
                              productos=productos,
                              servicios=servicios,
                              stats=stats)
                              
    except Exception as e:
        current_app.logger.error(f"Error al mostrar perfil de instructor: {str(e)}")
        flash(f'Error al cargar el perfil: {str(e)}', 'danger')
        return redirect(url_for('alumnos.index'))

@users.route('/debug_session')
def debug_session():
    """Debug route to check user authentication status"""
    if current_user.is_authenticated:
        user_type = "Client" if current_user.is_client() else "Instructor" if current_user.is_instructor() else "Unknown"
        return f"User is authenticated. Type: {user_type}, ID: {current_user.get_id()}, Name: {current_user.get_nombre()}"
    else:
        return "User is NOT authenticated."