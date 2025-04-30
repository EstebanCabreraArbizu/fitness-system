from flask_login import UserMixin
from flask import current_app
from app import login_manager
from app.db import get_db

class Client(UserMixin):
    def __init__(self, id, nombres, apellidos, celular, email, contrasenia, direccion, tipo_cliente, status, imagen,  fecha_pago=None, peso=None, altura=None, fecha_registro=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular
        self.email = email
        self.contrasenia = contrasenia
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.status = status
        self.imagen = imagen
        self.peso = peso
        self.altura = altura
        self.fecha_pago = fecha_pago  # Agregar este campo si es necesario
        self.fecha_registro = fecha_registro
        self._is_authenticated = True  # Agregar esta línea
    @property
    def is_authenticated(self):
        return self._is_authenticated
    def get_id(self):
        return f"c_{self.id}"
    def set_nombre(self, nombres):
        self.nombres = nombres
    def get_nombre(self):
        return self.nombres
    def set_imagen_url(self, image_url):
        self.imagen = image_url
    @staticmethod
    def get_by_id(user_id):
        try:
            # Convertir el user_id a entero si es un string
            if isinstance(user_id, str):
                if user_id.isdigit():
                    user_id = int(user_id)
                else:
                    return None
                    
            cur = get_db(current_app).cursor()
            cur.execute("""
            SELECT
                u.id,
                u.nombres,
                u.celular,
                u.email,
                u.contrasenia,
                u.direccion,
                u.tipo_cliente,
                u.status,
                u.apellidos,
                u.imagen
            FROM Cliente u
            WHERE u.id = %s
            """, (user_id,))
            user = cur.fetchone()
            cur.close()
            
            if user:
                return Client(
                    id=user['id'],
                    nombres=user['nombres'],
                    celular=user['celular'],
                    email=user['email'],
                    contrasenia=user['contrasenia'],
                    direccion=user['direccion'],
                    tipo_cliente=user['tipo_cliente'],
                    status=user['status'],
                    apellidos=user['apellidos'],
                    imagen=user['imagen']
                )
            return None
        except Exception as e:
            current_app.logger.error(f"Error en Client.get_by_id: {str(e)}")
            return None

    @staticmethod
    def get_by_email(email):
        cur = get_db(current_app).cursor()
        try:
            cur.execute("""
            SELECT
                u.id,
                u.nombres,
                u.celular,
                u.email,
                u.contrasenia,
                u.direccion,
                u.tipo_cliente,
                u.status,
                u.apellidos,
                u.imagen
            FROM Cliente u
            WHERE u.email = %s
            """, (email,))
            user = cur.fetchone()
            if user:
                return Client(
                    id=user['id'],
                    nombres=user['nombres'],
                    celular=user['celular'],
                    email=user['email'],
                    contrasenia=user['contrasenia'],
                    direccion=user['direccion'],
                    tipo_cliente=user['tipo_cliente'],
                    status=user['status'],
                    apellidos=user['apellidos'],
                    imagen=user['imagen']
                )
            return None
        finally:
            cur.close()
