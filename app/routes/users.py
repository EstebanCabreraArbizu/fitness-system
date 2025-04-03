import time
from datetime import timedelta
from urllib.parse import urlparse
from flask import Blueprint, request, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app.db import mysql
from app.models.user import User

users = Blueprint('users', __name__, template_folder='app/templates')


@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        next_url = request.args.get('next')
        if not next_url or not urlparse(next_url).scheme or urlparse(next_url).netloc != request.host:
            user_type_urls = {
                'Admin': url_for('admin.dashboard'),
                'Cliente': url_for('users.add_user'),
                'Propietario': url_for('owner.dashboard')
            }
            print(current_user.tipo_usuario)
            next_url = user_type_urls.get(current_user.tipo_usuario)
            if not next_url or next_url == None:
                time.sleep(0.5)
                flash(
                    'Tipo de usuario no reconocido. Por favor, contacte al administrador.', 'danger')
                return redirect(url_for('users.login'))
        return redirect(next_url)
    if request.method == 'GET':
        return render_template('users/login.html')

    correo = request.form['correo']
    contrasenia = request.form['contrasenia']
    if not correo or not contrasenia:
        flash('Por favor ingrese correo y contraseña', 'warning')
        return redirect(url_for('users.login'))
    try:
        cur = mysql.connection.cursor()
        # Consulta optimizada usando índices
        query = """
            SELECT
                u.id_usuario,
                u.nombre,
                u.correo,
                u.contrasenia,
                t.nombre as tipo_usuario,
                u.imagen_url
            FROM Usuario u
            INNER JOIN Tipo_usuario t ON u.Tipo_usuario_id_tipo_u = t.id_tipo_u
            WHERE u.correo = %s
            """

        cur.execute(query, (correo,))
        user_data = cur.fetchone()
        # Agregar print para debug
        print("Datos obtenidos:", user_data)
        print("Data type:", type(user_data), "Content:", user_data)
        cur.close()
        if user_data and str(user_data['contrasenia']) == str(contrasenia):
            user = User(
                id_usuario=int(user_data['id_usuario']),
                nombre=str(user_data['nombre']),
                correo=str(user_data['correo']),
                tipo_usuario=str(user_data['tipo_usuario']),
                imagen_url = str(user_data['imagen_url'])
            )
            # Recordar usuario por 7 día
            login_user(user, remember=True, duration=timedelta(days=7))

            flash(f'¡Bienvenido {user.nombre}!', 'success')

            # Obtener la URL a la que el usuario intentaba acceder
            next_url = request.args.get('next')
            if not next_url or not urlparse(next_url).scheme or urlparse(next_url).netloc != request.host:
                user_type_urls = {
                    'Admin': url_for('admin.dashboard'),
                    'Cliente': url_for('users.login'),
                    'Propietario': url_for('owner.dashboard')
                }
                next_url = user_type_urls.get(user.tipo_usuario)
                if not next_url:
                    time.sleep(0.5)
                    flash(
                        'Tipo de usuario no reconocido. Por favor, contacte al administrador.', 'danger')
                    return redirect(url_for('users.login'))
            return redirect(next_url)
        else:
            # Agregar pequeño delay para prevenir enumeración de usuarios
            time.sleep(0.5)
            flash('Usuario no encontrado o contrasenia incorrecta', 'danger')
            return redirect(url_for('users.login'))
    except Exception as e:
        flash('Error al iniciar sesión. Por favor intente más tarde.', 'danger')
        print(f"Error de login: {str(e)}")  # Log del er


@users.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
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
                
            # Hashear contraseña
            hashed_password = hash_password(contrasenia)
            
            # Imagen de perfil
            imagen_file = request.files.get('imagen')
            if imagen_file and imagen_file.filename:
                filename = secure_filename(imagen_file.filename)
                # Añadir timestamp para evitar colisiones
                name_parts = os.path.splitext(filename)
                filename = f"{name_parts[0]}_{int(time.time())}{name_parts[1]}"
                
                # Verificar tipo de archivo
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                if '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                    img_path = os.path.join('app/static/img', filename)
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
                        pass  # PIL no está disponible, mantener imagen original
                    
                    imagen = filename
                else:
                    flash('Formato de imagen no permitido. Use: png, jpg, jpeg, gif, webp', 'warning')
                    return redirect(url_for('users.add_user'))
            else:
                imagen = 'default-user.png'
            
            # Verificar si el correo ya existe
            conn = get_db(current_app)
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM Cliente WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El correo ya está registrado como Cliente', 'danger')
                return redirect(url_for('users.add_user'))
                
            cursor.execute("SELECT email FROM Instructor WHERE email = %s", (email,))
            if cursor.fetchone():
                flash('El correo ya está registrado como Instructor', 'danger')
                return redirect(url_for('users.add_user'))
                
            # Crear el usuario según el tipo seleccionado
            if tipo_usuario == 'Cliente':
                status = 1  # Por defecto activo
                
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
                """, (nombres, apellidos, celular, email, hashed_password, 
                      direccion, tipo_cliente, status, imagen, peso, altura))
                
                conn.commit()
                new_user_id = cursor.lastrowid
                
                # Crear el objeto Cliente para login
                user = Client(
                    id=new_user_id,
                    nombres=nombres,
                    apellidos=apellidos,
                    celular=celular,
                    email=email,
                    contrasenia=hashed_password,
                    direccion=direccion,
                    tipo_cliente=tipo_cliente,
                    status=status,
                    imagen=imagen
                )
                
            elif tipo_usuario == 'Instructor':
                status = 1  # Por defecto activo
                
                # Insertar en la tabla Instructor
                cursor.execute("""
                    INSERT INTO Instructor (nombres, apellidos, celular, email, contrasenia, 
                                           status, imagen) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (nombres, apellidos, celular, email, hashed_password, 
                      status, imagen))
                
                conn.commit()
                new_user_id = cursor.lastrowid
                
                # Crear el objeto Instructor para login
                user = Instructor(
                    id=new_user_id,
                    nombres=nombres,
                    apellidos=apellidos,
                    celular=celular,
                    email=email,
                    contrasenia=hashed_password,
                    status=status,
                    imagen=imagen
                )
            else:
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
            if 'conn' in locals() and conn:
                conn.rollback()
            import traceback
            error_details = traceback.format_exc()
            current_app.logger.error(f"Error al registrar usuario: {str(e)}\n{error_details}")
            flash('Error al registrar usuario. Por favor intente nuevamente.', 'danger')
            return redirect(url_for('users.add_user'))
        finally:
            if 'cursor' in locals() and cursor:
                cursor.close()
            if 'conn' in locals() and conn:
                conn.close()
                
    return render_template('users/create_account.html')

@users.route('/profile/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def config_account(id_usuario):
    cursor = mysql.connection.cursor()
    query = """
    SELECT u.*, t.nombre as tipo_usuario
    FROM Usuario u
    INNER JOIN Tipo_usuario t ON u.Tipo_usuario_id_tipo_u = t.id_tipo_u
    WHERE u.id_usuario = %s
	"""
    cursor.execute(query, (id_usuario,))
    user = cursor.fetchone()
    cursor.close()
    if request.method == 'GET':
        return render_template('users/config-account.html', user=user)
    else:
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        doc_identidad = request.form['doc_identidad']
        direccion = request.form['direccion']
        imagen_file = request.files.get('imagen')
        if imagen_file:
            filename = secure_filename(imagen_file.filename)
            imagen_file.save(f'app/static/img/{filename}')
            imagen_url = f'/static/img/{filename}'
        else:
            imagen_url = user['imagen_url']
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("""
                UPDATE Usuario SET 
                    nombre = %s,
                    telefono = %s,
                    doc_identidad = %s,
                    direccion = %s,
                    imagen_url = %s
                WHERE id_usuario = %s
            """, (nombre, telefono, doc_identidad, direccion, imagen_url, id_usuario))
            mysql.connection.commit()
            cursor.close()
            current_user.set_nombre(nombre)
            current_user.set_imagen_url(imagen_url)
            flash('Datos actualizados exitosamente', 'success')
            return redirect(url_for('users.config_account',  id_usuario = id_usuario))
        except Exception as e:
            mysql.connection.rollback()
            print(f"Error al actualizar datos: {str(e)}")
            flash(f'Error al actualizar datos: {str(e)}', 'danger')
@users.route('/edit_password/<int:id_usuario>', methods = ['POST'])
@login_required
def change_password(id_usuario):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT contrasenia FROM Usuario WHERE id_usuario = %s', (id_usuario,))
        user = cursor.fetchone()
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        if current_password == new_password:
            flash('La nueva contraseña no puede ser igual a la actual', 'warning')
            return redirect(url_for('users.config_account', id_usuario = id_usuario))
        else:
            cursor.execute(
                """
				UPDATE Usuario SET contrasenia = %s WHERE id_usuario = %s
				"""
                , (new_password, id_usuario)
				
			)
            cursor.connection.commit()
            cursor.close()
            flash('Contraseña actualizada exitosamente', 'success')
            return redirect(url_for('users.config_account', id_usuario = id_usuario))
    except Exception as e:
        mysql.connection.rollback()
        print(f"Error al actualizar contraseña: {str(e)}")
        flash(f'Error al actualizar contraseña: {str(e)}', 'danger')
        return redirect(url_for('users.config_account', id_usuario = id_usuario))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('users.login'))
