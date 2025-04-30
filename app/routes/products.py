from flask import Blueprint, render_template, request, flash, redirect, jsonify, current_app
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.db import get_db
from app.models.client import Client
from app.models.instructor import Instructor
from app.models.product import Product
import os
import time
products = Blueprint('product', __name__, template_folder='app/templates')


@products.route('/')
def index():
    try:
        # Verificar si el usuario está autenticado y es instructor
        user_id = current_user.id if current_user.is_authenticated and current_user.is_instructor() else None
        
        # Usar el modelo Product para obtener los productos
        product_list = Product.get_all(user_id=user_id)
        
        return render_template('productos/index.html', products=product_list)
    except Exception as e:
        current_app.logger.error(f'Error al cargar productos: {str(e)}')
        return render_template('productos/index.html', products=[], error="Error al cargar los productos")


@products.route('/all')
def get_all_products():
    """Obtiene todos los productos para cargar en la interfaz"""
    try:
        # Verificar si el usuario está autenticado y es instructor
        user_id = current_user.id if current_user.is_authenticated and current_user.is_instructor() else None
        
        # Usar el modelo Product para obtener los productos
        products_processed = Product.get_all(user_id=user_id)
        
        return jsonify({"success": True, "products": products_processed})
    except Exception as e:
        current_app.logger.error(f'Error al cargar productos: {str(e)}')
        return jsonify({"success": False, "error": str(e)})


@products.route('/instructors/all')
def get_all_instructors():
    """Obtiene todos los instructores para asignar a productos"""
    try:
        # Usar el modelo Product para obtener los instructores
        instructors = Product.get_all_instructors()
        
        return jsonify({"success": True, "instructors": instructors})
    except Exception as e:
        current_app.logger.error(f'Error al cargar instructores: {str(e)}')
        return jsonify({"success": False, "error": str(e)})


@products.route('/product/<int:id>')
def get_product(id):
    try:
        # Usar el modelo Product para obtener un producto específico
        product_dict = Product.get_by_id(id)
        
        if not product_dict:
            return jsonify({'error': 'Publicación no encontrada'}), 404
        
        return jsonify(product_dict)
    
    except Exception as e:
        current_app.logger.error(f"Error al obtener producto #{id}: {str(e)}")
        return jsonify({'error': 'Error al obtener datos de la publicación'}), 500


@products.route('/add_product', methods=['POST'])
def add_product():
    try:
        # Verificaciones detalladas para ayudar en la depuración
        current_app.logger.info("Form data received: %s", request.form)
        current_app.logger.info("Files received: %s", request.files)

        # Validar campos obligatorios
        required_fields = ['title', 'marca', 'palabras_claves']
        missing_fields = [
            field for field in required_fields if field not in request.form or not request.form[field].strip()]

        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Campos obligatorios faltantes: {", ".join(missing_fields)}'
            }), 400

        # Preparar datos del producto
        product_data = {
            'title': request.form['title'].strip(),
            'category': request.form.get('category', '').strip() or None,
            'description': request.form.get('description', '').strip() or None,
            'marca': request.form['marca'].strip(),
            'purchase_price': float(request.form.get('purchase_price') or 0),
            'price': float(request.form.get('price') or 0),
            'descuento': float(request.form.get('descuento') or 0),
            'previous_price': float(request.form.get('previous_price') or 0),
            'fecha_inicio': request.form.get('fecha_inicio') or None,
            'fecha_fin': request.form.get('fecha_fin') or None,
            'status': int(request.form.get('status') or 1),
            'palabras_claves': request.form['palabras_claves'].strip(),
            'relevant': int(request.form.get('relevant') == '1'),
            'outstanding': int(request.form.get('outstanding') == '1')
        }

        # Instructores
        if 'instructores[]' in request.form:
            product_data['instructores'] = [int(i) for i in request.form.getlist('instructores[]') if i and i.isdigit()]
        
        # Imágenes del producto
        image_files = None
        if 'productImages' in request.files:
            image_files = request.files.getlist('productImages')
        
        # Crear producto usando el modelo
        product_id = Product.create(product_data, image_files)
        
        if not product_id:
            return jsonify({'success': False, 'error': 'Error al crear el producto'}), 500
        
        # Obtener el producto recién creado
        new_product = Product.get_by_id(product_id)
        
        return jsonify({'success': True, 'product_id': product_id, 'product': new_product})
    
    except Exception as e:
        import traceback
        current_app.logger.error(f"Error al crear producto: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500


@products.route('/instructores')
def get_instructores():
    try:
        # Usar el modelo Product para obtener los instructores
        instructores = Product.get_all_instructors()
        
        result = []
        for instructor in instructores:
            # Intentar obtener Discipline_id
            conn = get_db(current_app)
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    SELECT Discipline_id FROM Discipline_Instructor 
                    WHERE Usuario_id = %s LIMIT 1
                """, (instructor['id'],))
                discipline_row = cursor.fetchone()
                discipline_id = discipline_row['Discipline_id'] if discipline_row else None
            except Exception as e:
                current_app.logger.error(f"Error al obtener disciplina: {str(e)}")
                discipline_id = None
            finally:
                cursor.close()
            
            # Crear objeto con el formato esperado por el frontend
            result.append({
                'id': instructor['id'],
                'nombres': instructor['nombre'],
                'apellidos': instructor['apellido'],
                'imagen': instructor['avatar'],
                'Discipline_id': discipline_id
            })
        
        return jsonify(result)
    except Exception as e:
        current_app.logger.error(f"Error al obtener instructores: {str(e)}")
        return jsonify([]), 500

@products.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    try:
        # Usar el modelo Product para eliminar un producto
        success = Product.delete(id)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'error': 'No se pudo eliminar el producto'})
    
    except Exception as e:
        current_app.logger.error(f"Error al eliminar producto: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@products.route('/update_product/<int:id>', methods=['POST'])
def update_product(id):
    try:
        # Verificar si el producto existe
        product = Product.get_by_id(id)
        
        if not product:
            return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
        
        # Validar campos obligatorios
        required_fields = ['title', 'marca', 'palabras_claves']
        missing_fields = [field for field in required_fields if field not in request.form or not request.form[field].strip()]
        
        if missing_fields:
            return jsonify({
                'success': False, 
                'error': f'Campos obligatorios faltantes: {", ".join(missing_fields)}'
            }), 400
        
        # Preparar datos del producto
        product_data = {
            'title': request.form['title'].strip(),
            'category': request.form.get('category', '').strip() or None,
            'description': request.form.get('description', '').strip() or None,
            'marca': request.form['marca'].strip(),
            'purchase_price': float(request.form.get('purchase_price') or 0),
            'price': float(request.form.get('price') or 0),
            'descuento': float(request.form.get('descuento') or 0),
            'previous_price': float(request.form.get('previous_price') or 0),
            'fecha_inicio': request.form.get('fecha_inicio') or None,
            'fecha_fin': request.form.get('fecha_fin') or None,
            'status': int(request.form.get('status') or 1),
            'palabras_claves': request.form['palabras_claves'].strip(),
            'relevant': int(request.form.get('relevant') == '1'),
            'outstanding': int(request.form.get('outstanding') == '1')
        }

        # Instructores
        if 'instructores[]' in request.form:
            product_data['instructores'] = [int(i) for i in request.form.getlist('instructores[]') if i and i.isdigit()]
        
        # Imágenes del producto
        image_files = None
        if 'productImages' in request.files:
            image_files = request.files.getlist('productImages')
        
        # Actualizar producto usando el modelo
        success = Product.update(id, product_data, image_files)
        
        if not success:
            return jsonify({'success': False, 'error': 'Error al actualizar el producto'}), 500
        
        # Obtener el producto actualizado
        updated_product = Product.get_by_id(id)
        
        return jsonify({'success': True, 'product': updated_product})
    
    except Exception as e:
        import traceback
        current_app.logger.error(f"Error al actualizar producto: {str(e)}")
        current_app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': str(e)}), 500