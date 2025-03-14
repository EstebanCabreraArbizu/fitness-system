from flask import Blueprint, render_template
from app.db import mysql
from app.models.user import User
import json

client = Blueprint('client', __name__, template_folder='app/templates')
@client.route('/', methods=['GET'])
def publications():
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT p.*, v.*, h.*, u.nombre as nombre_publicante 
        FROM Publicacion p 
        LEFT JOIN Vivienda h ON p.Vivienda_id_vivienda = h.id_vivienda 
        LEFT JOIN Vehiculo v ON p.Vehiculo_id_vehiculo = v.id_vehiculo
        LEFT JOIN Usuario u ON p.Usuario_id_usuario = u.id_usuario
    ''')
    pubs = cursor.fetchall()
    for pub in pubs:
        pub['imagenes'] = json.loads(pub['imagenes']) if pub['imagenes'] else []
    cursor.close()
    
    return render_template('clients/index.html', pubs = pubs)

@client.route('/publicacion/<int:id>')
def get_publication(id):
    try:
        cursor = mysql.connection.cursor()

        # Obtener datos básicos del usuario
        cursor.execute("""
            SELECT p.*, u.nombre as propietario
            FROM Publicacion p
            JOIN Usuario u ON p.Usuario_id_usuario = u.id_usuario
            WHERE p.id_publicacion = %s
        """, (id,))

        publicacion = cursor.fetchone()

        if not publicacion:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        # Convertir a diccionario

        publicacion_dict = {
            'id_publicacion': publicacion['id_publicacion'],
            'titulo': publicacion['titulo'],
            'descripcion': publicacion['descripcion'],
            'precio_unitario': publicacion['precio_unitario'],
            'fecha_publicacion': publicacion['fecha_publicacion'],
            'distrito': publicacion['distrito'],
            'direccion': publicacion['direccion'],
            'latitud': publicacion['latitud'],
            'longitud': publicacion['longitud'],
            'imagenes': publicacion['imagenes'],
            'estado': publicacion['estado'],
            'propietario': publicacion['propietario'],
            'vivienda_registrada': publicacion['Vivienda_id_vivienda'],
            'vehículo_registrado': publicacion['Vehiculo_id_vehiculo']
        }

        return jsonify(publicacion_dict)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error al obtener datos de la publicación'}), 500

    finally:
        cursor.close()

@client.route('/add_publication', methods=['GET', 'POST'])
#@login_required
def crear_publicacion():
    if request.method == 'GET':
        cursor = mysql.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Tipo_vivienda")
            tipos_vivienda = cursor.fetchall()
            cursor.execute("SELECT * FROM Ambiente")
            ambientes = cursor.fetchall()
            cursor.execute("SELECT * FROM Servicio")
            servicios = cursor.fetchall()
            cursor.execute("SELECT * FROM Tipo_vehiculo")
            tipos_vehiculo = cursor.fetchall()
            cursor.execute("SELECT * FROM Equipamiento")
            equipamientos = cursor.fetchall()
        except Exception as e:
            print("Error al obtener datos para los formularios: ", str(e))
            tipos_vivienda = ambientes = servicios = tipos_vehiculo = equipamientos = []
        finally:
            cursor.close()

        return render_template('owner/crear_publicacion.html', tipos_vivienda=tipos_vivienda, ambientes=ambientes, servicios=servicios, tipos_vehiculo=tipos_vehiculo, equipamientos=equipamientos)

    try:
        print("=== Iniciando creación de publicación ===")
        print(f"Datos del formulario: {request.form}")
        print(f"Archivos recibidos: {request.files}")

        cursor = mysql.connection.cursor()

        # Obtener datos del formulario
        tipo_publicacion = request.form['tipo_publicacion']
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        distrito = request.form['distrito']
        direccion = request.form['direccion']
        latitud = int(request.form['latitud'])
        longitud = int(request.form['longitud'])
        print(f"""
        Datos recibidos:
        - Tipo: {tipo_publicacion}
        - Título: {titulo}
        - Descripción: {descripcion}
        - Precio: {precio}
        - Distrito: {distrito}
        - Dirección: {direccion}
        """)

        # Procesar imágenes
        imagenes = request.files.getlist('imagenes[]')
        imagen_urls = []
        for imagen in imagenes:
            filename = secure_filename(imagen.filename)
            imagen.save(f'app/static/img/{filename}')
            imagen_urls.append(f'/static/img/{filename}')
        print(f"Imágenes recibidas: {len(imagenes)}")

        # Check if images are valid and not empty
        if not imagenes or any(imagen.filename == '' for imagen in imagenes):
            flash('Por favor, sube imágenes válidas.', 'error')
            return redirect(url_for('owner.crear_publicacion'))

        if tipo_publicacion == 'vivienda':

            # Extraer campos de vivienda
            fecha_construccion = request.form['fecha_construccion']
            dimensiones = request.form['dimensiones']
            antiguedad = request.form['antiguedad']
            tipo_vivienda = request.form['tipo_vivienda']

            print(f"""
            Datos de vivienda:
            - Fecha_construcción: {fecha_construccion}
			- Dimensiones: {dimensiones}
            - Antiguedad: {antiguedad}
            - Tipo_vivienda: {tipo_vivienda}
            """)

            cursor.execute(
                   """
                    INSERT INTO Vivienda (fecha_construccion, dimensiones, antiguedad, Tipo_vivienda_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (fecha_construccion, dimensiones, antiguedad, tipo_vivienda))

            cursor.execute("SELECT LAST_INSERT_ID()")
            vivienda_id = cursor.fetchone()[
                    'LAST_INSERT_ID()'] if 'LAST_INSERT_ID()' in cursor.description[0][0] else cursor.fetchone()[0]
            print(f"Vivienda creada con ID: {vivienda_id}")
            ambientes_sel = request.form.getlist('ambientes[]')
            for ambiente_id in ambientes_sel:
                    cursor.execute("""
                        INSERT INTO Ambiente_Vivienda (Ambiente_id, Vivienda_id)
                        VALUES (%s, %s)
                    """, (ambiente_id, vivienda_id))
            for servicio_id in request.form.getlist('servicios[]'):
                    cursor.execute("""
                        INSERT INTO Servicio_Vivienda (Servicio_id, Vivienda_id)
                        VALUES (%s, %s)
                    """, (servicio_id, vivienda_id))

        else:
            tipo_vehiculo = request.form['tipo_vehiculo']
            marca = request.form['marca']
            modelo = request.form['modelo']
            anio_text = request.form['anio']
            anio = int(anio_text.split('-')[0])
            placa = request.form['placa']
            color = request.form['color']
            transmision = request.form['transmision']
            cant_combustible = request.form['cant_combustible']
            tipo_combustible = request.form['tipo_combustible']
            kilometraje = request.form['kilometraje']
            seguro = request.form['seguro']

            print(f"""
            Datos de vehículo:
            - Tipo vehículo: {tipo_vehiculo}
            - Marca: {marca}
            - Modelo: {modelo}
            """)

            cursor.execute(
                """
                INSERT INTO Vehiculo (
                Tipo_vechiculo_id, marca, modelo, anio, placa, color, transmision,
                cant_combustible, tipo_combustible, kilometraje, Seguro_id_seguro) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (tipo_vehiculo, marca, modelo, anio, placa, color, transmision,
                 cant_combustible, tipo_combustible, kilometraje, seguro))
            print("Se realizó inserción en Vehículo")
            
            cursor.execute("SELECT LAST_INSERT_ID()")
            vehiculo_id = vehiculo_id = cursor.fetchone()['LAST_INSERT_ID()'] if 'LAST_INSERT_ID()' in cursor.description[0][0] else cursor.fetchone()[0]
            print(f"Vehículo creado con ID: {vehiculo_id}")
            equip_sel = request.form.getlist('equipamientos[]')
            for eq in equip_sel:
                cursor.execute(
                    """
                    INSERT INTO Equipamiento_Vehiculo (Vehiculo_id, Equipamiento_id)
                    VALUES (%s, %s)
                    """,
                    (vehiculo_id, eq))

        
        if tipo_publicacion == 'vivienda':
            cursor.execute("""
                    INSERT INTO Publicacion (
                        titulo, descripcion, precio_unitario, fecha_publicacion,
                        estado, latitud, longitud, distrito, direccion, imagenes, Usuario_id_usuario,
                        Vivienda_id_vivienda
                    ) VALUES (%s, %s, %s, NOW(), 'Activo',%s,%s, %s, %s, %s, %s, %s)
                """, (
                    titulo, descripcion, precio,latitud, longitud, distrito, direccion,
                    json.dumps(imagen_urls), current_user.id, vivienda_id
               ))
        else:
            cursor.execute("""
                    INSERT INTO Publicacion (
                        titulo, descripcion, precio_unitario, fecha_publicacion,
                        estado, latitud, longitud, distrito, direccion, imagenes, Usuario_id_usuario,
                        Vehiculo_id_vehiculo
                    ) VALUES (%s, %s, %s, NOW(), 'Activo',%s,%s, %s, %s, %s, %s, %s)
                """, (
                    titulo, descripcion, precio,latitud, longitud, distrito, direccion,
                    json.dumps(imagen_urls), current_user.id, vehiculo_id
                ))

        mysql.connection.commit()
        print("Publicación creada exitosamente")
        return jsonify({'success': True})

    except Exception as e:
        mysql.connection.rollback()
        print(f"Error general al crear publicación: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

    finally:
        if cursor:
            cursor.close()