from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models.product import Product, ProductImage
from app.forms.product import ProductForm
from app.extensions import db
from datetime import datetime
import os
import secrets
from werkzeug.utils import secure_filename

product_bp = Blueprint('product', __name__, url_prefix='/productos')

@product_bp.route('/products')
@login_required
def product_list():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category = request.args.get('category', type=int)
    status = request.args.get('status', type=str)
    
    query = Product.query.filter_by(user_id=current_user.id)
    
    if search:
        query = query.filter(
            db.or_(
                Product.title.ilike(f'%{search}%'),
                Product.description.ilike(f'%{search}%'),
                Product.palabras_claves.ilike(f'%{search}%')
            )
        )
    
    if category:
        query = query.filter_by(category=category)
        
    if status:
        query = query.filter_by(status=(status == 'active'))
    
    products = query.order_by(Product.date.desc()).paginate(page=page, per_page=12)
    
    return render_template('product/list.html', 
                         products=products,
                         search=search,
                         category=category,
                         status=status)

@product_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    if form.validate_on_submit():
        try:
            product = Product(
                title=form.title.data,
                category=form.category.data,
                description=form.description.data,
                marca=form.marca.data,
                purchase_price=form.purchase_price.data,
                price=form.price.data,
                descuento=form.descuento.data or 0,
                palabras_claves=form.palabras_claves.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                user_id=current_user.id,
                profesor=current_user.nombre_completo,
                profesor_foto=current_user.fotos[0].ruta if current_user.fotos else None,
                date=datetime.now().date(),
                status=1,
                relevant=1 if form.relevant.data else 0,
                outstanding=1 if form.outstanding.data else 0,
                additional=form.additional.data
            )
            
            db.session.add(product)
            db.session.flush()  # Para obtener el ID del producto
            
            # Manejo de imágenes
            if form.images.data:
                for image in form.images.data:
                    if image.filename:
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product.id))
                        os.makedirs(image_path, exist_ok=True)
                        image.save(os.path.join(image_path, filename))
                        
                        product_image = ProductImage(
                            image_name=filename,
                            product_id=product.id,
                            color_id=1  # Valor por defecto
                        )
                        db.session.add(product_image)
            
            db.session.commit()
            flash('Producto creado exitosamente', 'success')
            return redirect(url_for('product.product_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el producto: {str(e)}', 'error')
            return redirect(url_for('product.product_create'))
    
    return render_template('product/form.html', form=form)

@product_bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def product_edit(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id:
        flash('No tienes permiso para editar este producto', 'error')
        return redirect(url_for('product.product_list'))
    
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        try:
            product.title = form.title.data
            product.category = form.category.data
            product.description = form.description.data
            product.marca = form.marca.data
            product.purchase_price = form.purchase_price.data
            product.price = form.price.data
            product.descuento = form.descuento.data or 0
            product.palabras_claves = form.palabras_claves.data
            product.fecha_inicio = form.fecha_inicio.data
            product.fecha_fin = form.fecha_fin.data
            product.relevant = 1 if form.relevant.data else 0
            product.outstanding = 1 if form.outstanding.data else 0
            product.additional = form.additional.data
            
            # Manejo de imágenes
            if form.images.data:
                for image in form.images.data:
                    if image.filename:
                        filename = secure_filename(image.filename)
                        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product.id))
                        os.makedirs(image_path, exist_ok=True)
                        image.save(os.path.join(image_path, filename))
                        
                        product_image = ProductImage(
                            image_name=filename,
                            product_id=product.id,
                            color_id=1  # Valor por defecto
                        )
                        db.session.add(product_image)
            
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('product.product_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {str(e)}', 'error')
            return redirect(url_for('product.product_edit', id=id))
    
    # Inicializar los campos booleanos
    form.relevant.data = bool(product.relevant)
    form.outstanding.data = bool(product.outstanding)
    
    return render_template('product/form.html', form=form, product=product)

@product_bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def product_delete(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id:
        flash('No tienes permiso para eliminar este producto', 'error')
        return redirect(url_for('product.product_list'))
    
    try:
        # Eliminar imágenes del sistema de archivos
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product.id))
        if os.path.exists(image_path):
            for filename in os.listdir(image_path):
                os.remove(os.path.join(image_path, filename))
            os.rmdir(image_path)
        
        db.session.delete(product)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'error')
    
    return redirect(url_for('product.product_list'))

@product_bp.route('/products/<int:id>/images/<int:image_id>/delete', methods=['POST'])
@login_required
def product_delete_image(id, image_id):
    product = Product.query.get_or_404(id)
    image = ProductImage.query.get_or_404(image_id)
    
    if product.user_id != current_user.id or image.product_id != product.id:
        flash('No tienes permiso para eliminar esta imagen', 'error')
        return redirect(url_for('product.product_edit', id=id))
    
    try:
        # Eliminar la imagen del sistema de archivos
        image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'products', str(product.id), image.image_name)
        if os.path.exists(image_path):
            os.remove(image_path)
        
        db.session.delete(image)
        db.session.commit()
        flash('Imagen eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la imagen: {str(e)}', 'error')
    
    return redirect(url_for('product.product_edit', id=id))

@product_bp.route('/products/<int:id>/toggle-status', methods=['POST'])
@login_required
def product_toggle_status(id):
    product = Product.query.get_or_404(id)
    
    if product.user_id != current_user.id:
        flash('No tienes permiso para modificar este producto', 'error')
        return redirect(url_for('product.product_list'))
    
    try:
        product.status = 0 if product.status == 1 else 1
        db.session.commit()
        status = 'activado' if product.status == 1 else 'desactivado'
        flash(f'Producto {status} exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar el estado del producto: {str(e)}', 'error')
    
    return redirect(url_for('product.product_list'))

@product_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    """Agregar un nuevo producto"""
    if request.method == 'POST':
        try:
            # Validar campos requeridos
            required_fields = ['title', 'category', 'description', 'marca', 'purchase_price', 'price']
            for field in required_fields:
                if field not in request.form or not request.form[field]:
                    flash(f'El campo {field} es requerido', 'danger')
                    return redirect(url_for('product.nuevo_producto'))

            # Procesar imágenes
            imagenes = request.files.getlist('imagenes[]')
            rutas_imagenes = []
            
            if not imagenes or not any(imagen.filename for imagen in imagenes):
                flash('Debes subir al menos una imagen del producto', 'danger')
                return redirect(url_for('product.nuevo_producto'))
            
            for imagen in imagenes:
                if imagen and imagen.filename:
                    filename = f"product_{current_user.id}_{secrets.token_hex(8)}.{imagen.filename.rsplit('.', 1)[-1]}"
                    ruta = f'static/uploads/products/{filename}'
                    directorio = os.path.dirname(ruta)
                    if not os.path.exists(directorio):
                        os.makedirs(directorio)
                    imagen.save(ruta)
                    rutas_imagenes.append(ruta)
            
            # Obtener fechas con valores por defecto
            fecha_actual = datetime.now().date()
            fecha_inicio = request.form.get('fecha_inicio', fecha_actual)
            fecha_fin = request.form.get('fecha_fin', fecha_actual)
            
            # Obtener la foto del profesor (usar una por defecto si no existe)
            foto_profesor = getattr(current_user, 'foto_perfil', 'static/images/default_profile.png')
            
            # Crear el producto
            producto = Product(
                title=request.form['title'],
                category=int(request.form['category']),
                description=request.form['description'],
                marca=request.form['marca'],
                purchase_price=float(request.form['purchase_price']),
                price=float(request.form['price']),
                descuento=float(request.form.get('descuento', 0)),
                previous_price=float(request.form.get('previous_price', 0)),
                date=fecha_actual,
                user_id=current_user.id,
                status=1,  # Por defecto activo
                relevant=int(request.form.get('relevant', 0)),
                additional=request.form.get('additional', ''),
                outstanding=int(request.form.get('outstanding', 1)),
                palabras_claves=request.form.get('palabras_claves', ''),
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                profesor=current_user.nombre_completo,
                profesor_foto=foto_profesor
            )
            
            db.session.add(producto)
            db.session.flush()  # Para obtener el ID del producto
            
            # Agregar las imágenes
            for ruta in rutas_imagenes:
                imagen = ProductImage(
                    image_name=ruta,
                    color_id=1,  # Por defecto
                    product_id=producto.id
                )
                db.session.add(imagen)
            
            db.session.commit()
            flash('Producto agregado exitosamente', 'success')
            return redirect(url_for('product.lista_productos'))
            
        except ValueError as e:
            db.session.rollback()
            flash(f'Error en los datos ingresados: {str(e)}', 'danger')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al agregar el producto: {str(e)}', 'danger')
    
    return render_template('product/nuevo.html')

@product_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = Product.query.get_or_404(id)
    
    # Verificar que el usuario sea el propietario del producto
    if producto.user_id != current_user.id:
        flash('No tienes permiso para editar este producto', 'danger')
        return redirect(url_for('product.lista_productos'))
    
    if request.method == 'POST':
        try:
            # Validar campos requeridos
            campos_requeridos = ['title', 'category', 'description', 'marca', 'purchase_price', 'price']
            for campo in campos_requeridos:
                if not request.form.get(campo):
                    flash(f'El campo {campo} es requerido', 'danger')
                    return redirect(url_for('product.editar_producto', id=id))
            
            # Actualizar datos básicos
            producto.title = request.form['title']
            producto.category = int(request.form['category'])
            producto.description = request.form['description']
            producto.marca = request.form['marca']
            producto.purchase_price = float(request.form['purchase_price'])
            producto.price = float(request.form['price'])
            
            # Actualizar campos opcionales
            producto.descuento = float(request.form.get('descuento', 0))
            producto.previous_price = float(request.form.get('previous_price', 0))
            producto.palabras_claves = request.form.get('palabras_claves', '')
            producto.additional = request.form.get('additional', '')
            
            # Actualizar fechas si se proporcionan
            fecha_inicio = request.form.get('fecha_inicio')
            fecha_fin = request.form.get('fecha_fin')
            if fecha_inicio:
                producto.fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            if fecha_fin:
                producto.fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            
            # Actualizar flags
            producto.relevant = bool(request.form.get('relevant'))
            producto.outstanding = bool(request.form.get('outstanding'))
            
            # Procesar nuevas imágenes
            if 'imagenes[]' in request.files:
                imagenes = request.files.getlist('imagenes[]')
                for imagen in imagenes:
                    if imagen.filename:
                        filename = secure_filename(imagen.filename)
                        imagen.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                        nueva_imagen = ProductImage(image_name=filename, product_id=producto.id)
                        db.session.add(nueva_imagen)
            
            db.session.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('product.lista_productos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el producto: {str(e)}', 'danger')
            return redirect(url_for('product.editar_producto', id=id))
    
    return render_template('product/editar.html', producto=producto)

@product_bp.route('/<int:product_id>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(product_id):
    """Eliminar un producto"""
    producto = Product.query.get_or_404(product_id)
    
    if producto.user_id != current_user.id:
        flash('No tienes permiso para eliminar este producto', 'danger')
        return redirect(url_for('product.lista_productos'))
    
    try:
        # Eliminar las imágenes del sistema de archivos
        for imagen in producto.images:
            if os.path.exists(imagen.image_name):
                os.remove(imagen.image_name)
        
        db.session.delete(producto)
        db.session.commit()
        flash('Producto eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el producto: {str(e)}', 'danger')
    
    return redirect(url_for('product.lista_productos'))

@product_bp.route('/<int:product_id>/imagen/<int:imagen_id>/eliminar', methods=['POST'])
@login_required
def eliminar_imagen(product_id, imagen_id):
    """Eliminar una imagen de un producto"""
    producto = Product.query.get_or_404(product_id)
    imagen = ProductImage.query.get_or_404(imagen_id)
    
    if producto.user_id != current_user.id or imagen.product_id != producto.id:
        flash('No tienes permiso para eliminar esta imagen', 'danger')
        return redirect(url_for('product.lista_productos'))
    
    try:
        if os.path.exists(imagen.image_name):
            os.remove(imagen.image_name)
        db.session.delete(imagen)
        db.session.commit()
        flash('Imagen eliminada exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la imagen: {str(e)}', 'danger')
    
    return redirect(url_for('product.editar_producto', product_id=product_id)) 