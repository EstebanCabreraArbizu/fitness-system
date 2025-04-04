from flask import Blueprint, render_template, request, flash, redirect, jsonify, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.client import Client
from app.models.instructor import Instructor
import os
import time
products = Blueprint('product', __name__, template_folder='app/templates')


@products.route('/')
def index():
    conn = None
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        # Verifica si el usuario está autenticado antes de acceder a current_user.id
        if current_user.is_authenticated:
            # Para un instructor, muestra solo sus productos asociados
            if isinstance(current_user, Instructor):
                cursor.execute("""
                    SELECT p.* FROM Product p 
                    JOIN Instructor_Products ip ON p.id = ip.Product_id
                    WHERE ip.Instructor_id = %s
                """, (current_user.id,))
            else:
                # Para clientes o administradores, muestra todos los productos
                cursor.execute("SELECT * FROM Product WHERE status = 1")
        else:
            # Para usuarios no autenticados, muestra productos activos
            cursor.execute("SELECT * FROM Product WHERE status = 1")
            
        product_list = cursor.fetchall()
        
        # Procesar la lista de productos
        for product in product_list:
            if product['fecha_inicio']:
                product['fecha_inicio'] = product['fecha_inicio'].isoformat()
            if product['fecha_fin']:
                product['fecha_fin'] = product['fecha_fin'].isoformat()
                
            cursor.execute(
                "SELECT image_name FROM Product_images WHERE Product_id = %s", (product['id'],))
            product['images'] = [row['image_name'] for row in cursor.fetchall()]

            cursor.execute(
                "SELECT Instructor_id FROM Instructor_Products WHERE Product_id = %s", (product['id'],))
            product['instructores'] = [row['Instructor_id'] for row in cursor.fetchall()]
            
        return render_template('productos/index.html', products=product_list)
    except Exception as e:
        current_app.logger.error(f'Error al cargar productos: {str(e)}')
        return render_template('productos/index.html', products=[], error="Error al cargar los productos")
    finally:
        if cursor:
            cursor.close()


@products.route('/product/<int:id>')
def get_product(id):
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        # Obtener datos básicos del usuario
        cursor.execute("""
            SELECT *
            FROM Product
            WHERE id = %s
        """, (id,))

        product = cursor.fetchone()

        if not product:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        # Convertir a diccionario

        # Consultar imágenes asociadas
        cursor.execute(
            "SELECT image_name FROM Product_images WHERE Product_id = %s", (id,))
        images = [row['image_name'] for row in cursor.fetchall()]

        # Consultar instructores asignados
        cursor.execute("""
            SELECT DISTINCT i.id 
            FROM Instructor i 
            JOIN Instructor_Products ip ON i.id = ip.Instructor_id 
            WHERE ip.Product_id = %s
           """, (id,))
        instructores = [row['id'] for row in cursor.fetchall()]

        product_dict = {
            'id': product['id'],
            'title': product['title'],
            'category': product['category'],
            'description': product['description'],
            'marca': product['marca'],
            'purchase_price': product['purchase_price'],
            'price': product['price'],
            'descuento': product['descuento'],
            'previous_price': product['previous_price'],
            'fecha_inicio': product['fecha_inicio'].isoformat() if product['fecha_inicio'] else None,
            'fecha_fin': product['fecha_fin'].isoformat() if product['fecha_fin'] else None,
            'status': product['status'],
            'palabras_claves': product['palabras_claves'],
            'relevant': product['relevant'],
            'outstanding': product['outstanding'],
            'images': images,
            'instructores': instructores
        }

        return jsonify(product_dict)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error al obtener datos de la publicación'}), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            cursor.close()


@products.route('/add_product', methods=['POST'])
def add_product():
    cursor = None
    try:
        # Verificaciones detalladas para ayudar en la depuración
        print("Form data received:", request.form)
        print("Files received:", request.files)

        # Validar campos obligatorios
        required_fields = ['title', 'marca', 'palabras_claves']
        missing_fields = [
            field for field in required_fields if field not in request.form or not request.form[field].strip()]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos obligatorios faltantes: {", ".join(missing_fields)}'
            }), 400

        # Extraer datos del formulario (con validación)
        title = request.form['title'].strip()
        category = request.form.get('category', '').strip() or None
        description = request.form.get('description', '').strip() or None
        marca = request.form['marca'].strip()

        # Convertir valores numéricos con manejo de errores
        try:
            purchase_price = float(request.form.get('purchase_price') or 0)
            price = float(request.form.get('price') or 0)
            descuento = float(request.form.get('descuento') or 0)
            previous_price = float(request.form.get('previous_price') or 0)
        except ValueError as e:
            return jsonify({'success': False, 'error': f'Error en valor numérico: {str(e)}'}), 400

        # Otros campos
        fecha_inicio = request.form.get('fecha_inicio') or None
        fecha_fin = request.form.get('fecha_fin') or None
        status = int(request.form.get('status') or 1)
        palabras_claves = request.form['palabras_claves'].strip()

        # Checkboxes
        relevant = int(request.form.get('relevant') == '1')
        outstanding = int(request.form.get('outstanding') == '1')

        # Procesar imágenes del producto
        image_names = []
        if 'productImages' in request.files:
            # Depuración para ver qué estamos recibiendo
            print("Archivos recibidos:", request.files.getlist('productImages'))
            print("Cantidad de archivos:", len(request.files.getlist('productImages')))
            imagenes = request.files.getlist('productImages')
            for i, imagen in enumerate(imagenes):
                print(f"Procesando imagen {i+1}: {imagen.filename}")
                if imagen.filename:
                    filename = secure_filename(imagen.filename)
                    # Asegurarse de que el nombre de archivo sea único
                    base, extension = os.path.splitext(filename)
                    unique_filename = f"{base}_{int(time.time())}_{i}{extension}"
                    imagen.save(f'app/static/img/{filename}')
                    image_names.append(filename)
                    try:
                        imagen.save(f'app/static/img/{unique_filename}')
                        image_names.append(unique_filename)
                        print(f"Imagen guardada: {unique_filename}")
                    except Exception as e:
                        print(f"Error al guardar imagen: {str(e)}")

        # Instructores
        instructores = []
        if 'instructores[]' in request.form:
            instructores = [int(i) for i in request.form.getlist('instructores[]') if i and i.isdigit()]
        
        # Operaciones en la base de datos
        conn = get_db(current_app)
        cursor = conn.cursor()
        # Insertar producto
        cursor.execute(
            """
            INSERT INTO Product (
                title, category, description, marca, purchase_price, price, descuento,
                previous_price, fecha_inicio, fecha_fin, status, palabras_claves, relevant, outstanding, date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                title, category, description, marca, purchase_price, price, descuento,
                previous_price, fecha_inicio, fecha_fin, status, palabras_claves, relevant, outstanding
            )
        )
        conn.commit()
        
        # Obtener ID insertado
        cursor.execute("SELECT LAST_INSERT_ID() as id")
        product_id = cursor.fetchone()['id']
        
        # Insertar imágenes
        for img in image_names:
            cursor.execute(
                "INSERT INTO Product_images (image_name, color_id, Product_id) VALUES (%s, %s, %s)",
                (img, 0, product_id)
            )
        
        # Insertar instructores
        for instructor_id in instructores:
            cursor.execute(
                "INSERT INTO Instructor_Products (Instructor_id, Product_id) VALUES (%s, %s)",
                (instructor_id, product_id)
            )
        
        conn.commit()
        
        # Consultar el producto recién creado
        cursor.execute("SELECT * FROM Product WHERE id = %s", (product_id,))
        new_product = cursor.fetchone()
        
        # Convertir fechas para la respuesta JSON
        if new_product['fecha_inicio']:
            new_product['fecha_inicio'] = new_product['fecha_inicio'].isoformat()
        if new_product['fecha_fin']:
            new_product['fecha_fin'] = new_product['fecha_fin'].isoformat()
        
        # Consultar imágenes e instructores
        cursor.execute("SELECT image_name FROM Product_images WHERE Product_id = %s", (product_id,))
        new_product['images'] = [row['image_name'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT Instructor_id FROM Instructor_Products WHERE Product_id = %s", (product_id,))
        new_product['instructores'] = [row['Instructor_id'] for row in cursor.fetchall()]
        
        return jsonify({'success': True, 'product_id': product_id, 'product': new_product})
    
    except Exception as e:
        if conn:
            conn.rollback()
        import traceback
        print(f"Error al crear producto: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@products.route('/instructores')
def get_instructores():
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                i.id, i.nombres, i.apellidos, i.imagen, 
                (SELECT Discipline_id FROM Discipline_Instructor WHERE Instructor_id = i.id LIMIT 1) as Discipline_id
            FROM Instructor i
            WHERE i.status = 1
        """)
        instructores = cursor.fetchall()
        
        #JSON
        result = []
        for instructor in instructores:
            result.append({
                'id': instructor['id'],
                'nombres': instructor['nombres'],
                'apellidos': instructor['apellidos'],
                'imagen': instructor['imagen'],
                'Discipline_id': instructor['Discipline_id']
            })
        return jsonify(result)
    except Exception as e:
        print(f"Error al obtener instructores: {str(e)}")
        return jsonify([]), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@products.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    cursor = None
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        # Primero eliminar registros relacionados
        cursor.execute("DELETE FROM Product_images WHERE Product_id = %s", (id,))
        cursor.execute("DELETE FROM Instructor_Products WHERE Product_id = %s", (id,))
        
        # Luego eliminar el producto
        cursor.execute("DELETE FROM Product WHERE id = %s", (id,))
        conn.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        conn.rollback()
        print(f"Error al eliminar producto: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})
    
    finally:
        if cursor:
            cursor.close()

@products.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):
    cursor = None
    try:
        # Verificar si el producto existe
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Product WHERE id = %s", (id,))
        existing_product = cursor.fetchone()
        
        if not existing_product:
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
        
        
        required_fields = ['title', 'marca', 'palabras_claves']
        missing_fields = [field for field in required_fields if field not in request.form or not request.form[field].strip()]
        
        if missing_fields:
            return jsonify({
                'success': False, 
                'error': f'Campos obligatorios faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Extraer datos del formulario
        title = request.form['title'].strip()
        category = request.form.get('category', '').strip() or None
        description = request.form.get('description', '').strip() or None
        marca = request.form['marca'].strip()
        
        # Convertir valores numéricos
        try:
            purchase_price = float(request.form.get('purchase_price') or 0)
            price = float(request.form.get('price') or 0)
            descuento = float(request.form.get('descuento') or 0)
            previous_price = float(request.form.get('previous_price') or 0)
        except ValueError as e:
            return jsonify({'success': False, 'error': f'Error en valor numérico: {str(e)}'}), 400
        
        # Otros campos
        fecha_inicio = request.form.get('fecha_inicio') or None
        fecha_fin = request.form.get('fecha_fin') or None
        status = int(request.form.get('status') or 1)
        palabras_claves = request.form['palabras_claves'].strip()
        
        # Checkboxes
        relevant = int(request.form.get('relevant') == '1')
        outstanding = int(request.form.get('outstanding') == '1')
        
        # Actualizar el producto en la base de datos
        cursor.execute("""
            UPDATE Product SET
                title = %s, category = %s, description = %s, marca = %s,
                purchase_price = %s, price = %s, descuento = %s, previous_price = %s,
                fecha_inicio = %s, fecha_fin = %s, status = %s, palabras_claves = %s, 
                relevant = %s, outstanding = %s
            WHERE id = %s
        """, (
            title, category, description, marca, purchase_price, price, descuento,
            previous_price, fecha_inicio, fecha_fin, status, palabras_claves, relevant, outstanding, id
        ))
        
        # Procesar imágenes del producto (solo si se envían nuevas)
        if 'productImages' in request.files:
            imagenes = request.files.getlist('productImages')
            for imagen in imagenes:
                if imagen.filename:
                    filename = secure_filename(imagen.filename)
                    imagen.save(f'app/static/img/{filename}')
                    cursor.execute(
                        "INSERT INTO Product_images (image_name, color_id, Product_id) VALUES (%s, %s, %s)",
                        (filename, 0, id)
                    )
        
        # Procesar instructores
        # Primero eliminar las relaciones existentes
        cursor.execute("DELETE FROM Instructor_Products WHERE Product_id = %s", (id,))
        
        # Luego agregar las nuevas
        if 'instructores[]' in request.form:
            instructores = [int(i) for i in request.form.getlist('instructores[]') if i and i.isdigit()]
            for instructor_id in instructores:
                cursor.execute(
                    "INSERT INTO Instructor_Products (Instructor_id, Product_id) VALUES (%s, %s)",
                    (instructor_id, id)
                )
        
        conn.commit()
        
        # Obtener el producto actualizado
        cursor.execute("SELECT * FROM Product WHERE id = %s", (id,))
        updated_product = cursor.fetchone()
        
        # Convertir fechas para JSON
        if updated_product['fecha_inicio']:
            updated_product['fecha_inicio'] = updated_product['fecha_inicio'].isoformat()
        if updated_product['fecha_fin']:
            updated_product['fecha_fin'] = updated_product['fecha_fin'].isoformat()
        
        # Consultar imágenes e instructores
        cursor.execute("SELECT image_name FROM Product_images WHERE Product_id = %s", (id,))
        updated_product['images'] = [row['image_name'] for row in cursor.fetchall()]
        
        cursor.execute("SELECT Instructor_id FROM Instructor_Products WHERE Product_id = %s", (id,))
        updated_product['instructores'] = [row['Instructor_id'] for row in cursor.fetchall()]
        
        return jsonify({'success': True, 'product': updated_product})
    
    except Exception as e:
        if conn:
            conn.rollback()
        import traceback
        print(f"Error al actualizar producto: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()