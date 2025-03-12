from flask_login import UserMixin
from app import login_manager
from app.db import mysql

class Client(UserMixin):
    def __init__(self, id_usuario, nombres, celular, email, contrasenia, direccion, tipo_cliente, status,apellidos, imagen):
        self.id = id_usuario
        self.nombres = nombres
        self.celular = celular
        self.email = email
        self.contrasenia = contrasenia
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.status = status
        self.apellidos = apellidos
        self.imagen = imagen
        self._is_authenticated = True  # Agregar esta línea
    @property
    def is_authenticated(self):
        return self._is_authenticated
    def get_id(self):
        return str(self.id)
    def set_nombre(self, nombres):
        self.nombres = nombres
    def set_imagen_url(self, image_url):
        self.imagen = image_url
    @staticmethod
    def get_by_id(user_id):
        cur = mysql.connection.cursor()
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
            WHERE u.id = %s
            """, (user_id,))
            user = cur.fetchone()
            if user:
                return Client(
                    id_usuario=user['id'],
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

    @staticmethod
    def get_by_email(email):
        cur = mysql.connection.cursor()
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
                    id_usuario=user['id'],
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

@login_manager.user_loader
def load_user(user_id):
    return Client.get_by_id(user_id)
