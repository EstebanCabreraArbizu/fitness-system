from flask_login import UserMixin
from app import login_manager
from app.db import get_db
from flask import current_app

class Instructor(UserMixin):
    def __init__(self, id, nombres, celular, email, contrasenia, status,apellidos, imagen):
        self.id = id
        self.nombres = nombres
        self.celular = celular
        self.email = email
        self.contrasenia = contrasenia
        self.status = status
        self.apellidos = apellidos
        self.imagen = imagen
        self._is_authenticated = True  # Agregar esta línea
    @property
    def is_authenticated(self):
        return self._is_authenticated
    def get_id(self):
        return str(self.id)
    def set_nombre(self, nombre):
        self.nombres = nombre
    def get_nombre(self):
        return self.nombres
    def set_imagen_url(self, image_url):
        self.imagen = image_url
    # Corregir el método get_by_id

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
                u.status,
                u.apellidos,
                u.imagen
            FROM Instructor u
            WHERE u.id = %s
            """, (user_id,))
            user = cur.fetchone()
            cur.close()
            
            if user:
                return Instructor(
                    id=user['id'],
                    nombres=user['nombres'],
                    celular=user['celular'],
                    email=user['email'],
                    contrasenia=user['contrasenia'],
                    status=user['status'],
                    apellidos=user['apellidos'],
                    imagen=user['imagen']
                )
            return None
        except Exception as e:
            current_app.logger.error(f"Error en Instructor.get_by_id: {str(e)}")
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
                u.status,
                u.apellidos,
                u.imagen
            FROM Instructor u
            WHERE u.email = %s
            """, (email,))
            user = cur.fetchone()
            if user:
                return Instructor(
                    id=user['id'],
                    nombres=user['nombres'],
                    celular=user['celular'],
                    email=user['email'],
                    contrasenia=user['contrasenia'],
                    status=user['status'],
                    apellidos=user['apellidos'],
                    imagen=user['imagen']
                )
            return None
        finally:
            cur.close()

@login_manager.user_loader
def load_user(user_id):
    return Instructor.get_by_id(user_id)
