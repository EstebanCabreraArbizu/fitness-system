from flask import current_app
import os
from werkzeug.utils import secure_filename
import time
from app.db import get_db

class Product:
    def __init__(self, id=None, title=None, category=None, description=None, 
                 marca=None, purchase_price=None, price=None, descuento=None,
                 previous_price=None, date=None, user_id=None, status=1,
                 relevant=0, additional=None, outstanding=1, palabras_claves=None,
                 fecha_inicio=None, fecha_fin=None):
        self.id = id
        self.title = title
        self.category = category
        self.description = description
        self.marca = marca
        self.purchase_price = purchase_price
        self.price = price
        self.descuento = descuento
        self.previous_price = previous_price
        self.date = date
        self.user_id = user_id
        self.status = status
        self.relevant = relevant
        self.additional = additional
        self.outstanding = outstanding
        self.palabras_claves = palabras_claves
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.images = []
        self.instructores = []
    
    @staticmethod
    def get_all(user_id=None, only_active=True):
        """Obtiene todos los productos, con opción para filtrar por instructor o solo activos"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            if user_id and user_id > 0:
                # Para un instructor, muestra solo sus productos asociados
                cursor.execute("""
                    SELECT p.* FROM Product p 
                    JOIN Instructor_Products ip ON p.id = ip.Product_id
                    WHERE ip.Usuario_id = %s
                """, (user_id,))
            else:
                # Para otros usuarios, muestra todos los productos o solo activos
                if only_active:
                    cursor.execute("SELECT * FROM Product WHERE status = 1")
                else:
                    cursor.execute("SELECT * FROM Product")
            
            products = cursor.fetchall()
            
            # Procesar cada producto para incluir imágenes e instructores
            result = []
            for product in products:
                product_dict = dict(product)
                
                # Convertir fechas a formato ISO para JSON
                if product_dict['fecha_inicio']:
                    product_dict['fecha_inicio'] = product_dict['fecha_inicio'].isoformat()
                if product_dict['fecha_fin']:
                    product_dict['fecha_fin'] = product_dict['fecha_fin'].isoformat()
                if product_dict['date']:
                    product_dict['date'] = product_dict['date'].isoformat()
                
                # Obtener imágenes del producto
                cursor.execute(
                    "SELECT image_name FROM Product_images WHERE Product_id = %s", 
                    (product_dict['id'],)
                )
                product_dict['images'] = [row['image_name'] for row in cursor.fetchall()]
                
                # Obtener instructores asignados
                cursor.execute(
                    "SELECT Usuario_id FROM Instructor_Products WHERE Product_id = %s", 
                    (product_dict['id'],)
                )
                product_dict['instructores'] = [row['Usuario_id'] for row in cursor.fetchall()]
                
                result.append(product_dict)
            
            return result
        except Exception as e:
            current_app.logger.error(f"Error al obtener productos: {str(e)}")
            return []
        finally:
            cursor.close()
    
    @staticmethod
    def get_by_id(product_id):
        """Obtiene un producto por su ID con sus imágenes e instructores"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Obtener datos básicos del producto
            cursor.execute("SELECT * FROM Product WHERE id = %s", (product_id,))
            product = cursor.fetchone()
            
            if not product:
                return None
            
            # Convertir a diccionario para facilitar manipulación
            product_dict = dict(product)
            
            # Convertir fechas a formato ISO para JSON
            if product_dict['fecha_inicio']:
                product_dict['fecha_inicio'] = product_dict['fecha_inicio'].isoformat()
            if product_dict['fecha_fin']:
                product_dict['fecha_fin'] = product_dict['fecha_fin'].isoformat()
            if product_dict['date']:
                product_dict['date'] = product_dict['date'].isoformat()
            
            # Obtener imágenes del producto
            cursor.execute(
                "SELECT image_name FROM Product_images WHERE Product_id = %s", 
                (product_id,)
            )
            product_dict['images'] = [row['image_name'] for row in cursor.fetchall()]
            
            # Obtener instructores asignados
            cursor.execute("""
                SELECT Usuario_id 
                FROM Instructor_Products 
                WHERE Product_id = %s
            """, (product_id,))
            product_dict['instructores'] = [row['Usuario_id'] for row in cursor.fetchall()]
            
            return product_dict
        except Exception as e:
            current_app.logger.error(f"Error al obtener producto #{product_id}: {str(e)}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def create(product_data, image_files=None):
        """Crea un nuevo producto con sus imágenes e instructores"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Insertar producto
            cursor.execute("""
                INSERT INTO Product (
                    title, category, description, marca, purchase_price, price, descuento,
                    previous_price, fecha_inicio, fecha_fin, status, palabras_claves, 
                    relevant, outstanding, date
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
            """, (
                product_data.get('title'),
                product_data.get('category'),
                product_data.get('description'),
                product_data.get('marca'),
                product_data.get('purchase_price', 0),
                product_data.get('price', 0),
                product_data.get('descuento', 0),
                product_data.get('previous_price', 0),
                product_data.get('fecha_inicio'),
                product_data.get('fecha_fin'),
                product_data.get('status', 1),
                product_data.get('palabras_claves'),
                product_data.get('relevant', 0),
                product_data.get('outstanding', 1)
            ))
            
            # Obtener ID del producto recién creado
            product_id = cursor.lastrowid
            
            # Guardar imágenes si hay
            if image_files and len(image_files) > 0:
                for i, image in enumerate(image_files):
                    if image.filename:
                        filename = secure_filename(image.filename)
                        base, extension = os.path.splitext(filename)
                        unique_filename = f"{base}_{int(time.time())}_{i}{extension}"
                        
                        try:
                            # Guardar imagen en la carpeta static/img
                            image.save(f'app/static/img/{unique_filename}')
                            
                            # Guardar referencia en la base de datos
                            cursor.execute("""
                                INSERT INTO Product_images (image_name, color_id, Product_id)
                                VALUES (%s, %s, %s)
                            """, (unique_filename, 0, product_id))
                        except Exception as e:
                            current_app.logger.error(f"Error al guardar imagen: {str(e)}")
            
            # Asignar instructores si hay
            instructores = product_data.get('instructores', [])
            if instructores and len(instructores) > 0:
                for instructor_id in instructores:
                    cursor.execute("""
                        INSERT INTO Instructor_Products (Usuario_id, Product_id)
                        VALUES (%s, %s)
                    """, (instructor_id, product_id))
            
            conn.commit()
            return product_id
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al crear producto: {str(e)}")
            return None
        finally:
            cursor.close()
    
    @staticmethod
    def update(product_id, product_data, image_files=None):
        """Actualiza un producto existente con sus imágenes e instructores"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Verificar que el producto exista
            cursor.execute("SELECT id FROM Product WHERE id = %s", (product_id,))
            if not cursor.fetchone():
                return False
            
            # Actualizar producto
            cursor.execute("""
                UPDATE Product SET
                    title = %s,
                    category = %s,
                    description = %s,
                    marca = %s,
                    purchase_price = %s,
                    price = %s,
                    descuento = %s,
                    previous_price = %s,
                    fecha_inicio = %s,
                    fecha_fin = %s,
                    status = %s,
                    palabras_claves = %s,
                    relevant = %s,
                    outstanding = %s
                WHERE id = %s
            """, (
                product_data.get('title'),
                product_data.get('category'),
                product_data.get('description'),
                product_data.get('marca'),
                product_data.get('purchase_price', 0),
                product_data.get('price', 0),
                product_data.get('descuento', 0),
                product_data.get('previous_price', 0),
                product_data.get('fecha_inicio'),
                product_data.get('fecha_fin'),
                product_data.get('status', 1),
                product_data.get('palabras_claves'),
                product_data.get('relevant', 0),
                product_data.get('outstanding', 1),
                product_id
            ))
            
            # Guardar nuevas imágenes si hay
            if image_files and len(image_files) > 0:
                for i, image in enumerate(image_files):
                    if image.filename:
                        filename = secure_filename(image.filename)
                        base, extension = os.path.splitext(filename)
                        unique_filename = f"{base}_{int(time.time())}_{i}{extension}"
                        
                        try:
                            # Guardar imagen en la carpeta static/img
                            image.save(f'app/static/img/{unique_filename}')
                            
                            # Guardar referencia en la base de datos
                            cursor.execute("""
                                INSERT INTO Product_images (image_name, color_id, Product_id)
                                VALUES (%s, %s, %s)
                            """, (unique_filename, 0, product_id))
                        except Exception as e:
                            current_app.logger.error(f"Error al guardar imagen: {str(e)}")
            
            # Actualizar instructores (eliminar todos y añadir nuevos)
            cursor.execute("DELETE FROM Instructor_Products WHERE Product_id = %s", (product_id,))
            
            instructores = product_data.get('instructores', [])
            if instructores and len(instructores) > 0:
                for instructor_id in instructores:
                    cursor.execute("""
                        INSERT INTO Instructor_Products (Usuario_id, Product_id)
                        VALUES (%s, %s)
                    """, (instructor_id, product_id))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al actualizar producto #{product_id}: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def delete(product_id):
        """Elimina un producto y sus relaciones"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Eliminar primero las referencias en otras tablas
            cursor.execute("DELETE FROM Product_images WHERE Product_id = %s", (product_id,))
            cursor.execute("DELETE FROM Instructor_Products WHERE Product_id = %s", (product_id,))
            
            # Luego eliminar el producto
            cursor.execute("DELETE FROM Product WHERE id = %s", (product_id,))
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            current_app.logger.error(f"Error al eliminar producto #{product_id}: {str(e)}")
            return False
        finally:
            cursor.close()
    
    @staticmethod
    def get_all_instructors():
        """Obtiene todos los instructores disponibles para asignar a productos"""
        conn = get_db(current_app)
        cursor = conn.cursor()
        
        try:
            # Modificar la consulta para usar directamente Tipo_usuario_id = 2 (instructor)
            # en lugar de buscar por nombre
            cursor.execute("""
                SELECT u.id, u.nombres as nombre, u.apellidos as apellido, u.imagen as avatar
                FROM Usuario u
                WHERE u.Tipo_usuario_id = 2 AND u.status = 1
            """)
            
            instructors = cursor.fetchall()
            
            # Si no hay instructores, crear una lista de respaldo vacía
            if not instructors:
                current_app.logger.warning("No se encontraron instructores en la base de datos")
                return []
                
            return [dict(instructor) for instructor in instructors]
        except Exception as e:
            current_app.logger.error(f"Error al obtener instructores: {str(e)}")
            return []
        finally:
            if cursor:
                cursor.close() 