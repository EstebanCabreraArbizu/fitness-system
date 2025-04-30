from flask_login import UserMixin
from flask import current_app
from app import login_manager
from app.db import get_db

class User(UserMixin):
    def __init__(self, id, nombres, apellidos, celular, email, contrasenia, 
                 status, imagen, tipo_usuario_id, fecha_registro=None, direccion=None, 
                 tipo_cliente=None, nivel_actividad=None, peso=None, altura=None, 
                 fecha_pago=None, certificaciones=None, especialidad=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.celular = celular
        self.email = email
        self.contrasenia = contrasenia
        self.status = status
        self.imagen = imagen
        self.tipo_usuario_id = tipo_usuario_id
        self.fecha_registro = fecha_registro
        # Cliente attributes
        self.direccion = direccion
        self.tipo_cliente = tipo_cliente
        self.nivel_actividad = nivel_actividad
        self.peso = peso
        self.altura = altura
        self.fecha_pago = fecha_pago
        # Instructor attributes
        self.certificaciones = certificaciones
        self.especialidad = especialidad
        self._is_authenticated = True
    
    @property
    def is_authenticated(self):
        return self._is_authenticated
    
    def get_id(self):
        return f"u_{self.id}"
    
    def set_nombre(self, nombres):
        self.nombres = nombres
    
    def get_nombre(self):
        return self.nombres
    
    def set_imagen_url(self, image_url):
        self.imagen = image_url
    
    def is_instructor(self):
        return self.tipo_usuario_id == 2  # Ajustar según valor en tabla Tipo_usuario
    
    def is_client(self):
        return self.tipo_usuario_id == 1  # Ajustar según valor en tabla Tipo_usuario
    
    @staticmethod
    def get_by_id(user_id):
        try:
            # Convertir el user_id a entero eliminando el prefijo
            if isinstance(user_id, str) and user_id.startswith('u_'):
                user_id = int(user_id[2:])
                    
            cur = get_db(current_app).cursor()
            cur.execute("""
            SELECT
                u.*,
                IFNULL((SELECT direccion FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as direccion,
                IFNULL((SELECT tipo_cliente FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as tipo_cliente,
                IFNULL((SELECT nivel_actividad FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as nivel_actividad,
                IFNULL((SELECT peso FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as peso,
                IFNULL((SELECT altura FROM Historial_Medidas WHERE Usuario_id = u.id ORDER BY fecha_medicion DESC LIMIT 1), NULL) as altura,
                IFNULL((SELECT certificaciones FROM Instructor_datos WHERE Usuario_id = u.id), NULL) as certificaciones,
                IFNULL((SELECT especialidad FROM Instructor_datos WHERE Usuario_id = u.id), NULL) as especialidad
            FROM Usuario u
            WHERE u.id = %s
            """, (user_id,))
            user_data = cur.fetchone()
            cur.close()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    nombres=user_data['nombres'],
                    apellidos=user_data['apellidos'],
                    celular=user_data['celular'],
                    email=user_data['email'],
                    contrasenia=user_data['contrasenia'],
                    status=user_data['status'],
                    imagen=user_data['imagen'],
                    tipo_usuario_id=user_data['Tipo_usuario_id'],
                    fecha_registro=user_data['fecha_registro'],
                    direccion=user_data['direccion'],
                    tipo_cliente=user_data['tipo_cliente'],
                    nivel_actividad=user_data['nivel_actividad'],
                    peso=user_data['peso'],
                    altura=user_data['altura'],
                    certificaciones=user_data['certificaciones'],
                    especialidad=user_data['especialidad']
                )
            return None
        except Exception as e:
            current_app.logger.error(f"Error en User.get_by_id: {str(e)}")
            return None

    @staticmethod
    def get_by_email(email):
        cur = get_db(current_app).cursor()
        try:
            cur.execute("""
            SELECT
                u.id, u.nombres, u.apellidos, u.celular, u.email, 
                u.contrasenia, u.status, u.imagen, u.fecha_registro,
                u.Tipo_usuario_id,
                IFNULL((SELECT direccion FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as direccion,
                IFNULL((SELECT tipo_cliente FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as tipo_cliente,
                IFNULL((SELECT peso FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as peso,
                IFNULL((SELECT altura FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as altura,
                IFNULL((SELECT fecha_pago FROM Cliente_datos WHERE Usuario_id = u.id), NULL) as fecha_pago
            FROM Usuario u
            WHERE u.email = %s AND u.status = 1
            """, (email,))
            user_data = cur.fetchone()
            
            if user_data:
                return User(
                    id=user_data['id'],
                    nombres=user_data['nombres'],
                    apellidos=user_data['apellidos'],
                    celular=user_data['celular'],
                    email=user_data['email'],
                    contrasenia=user_data['contrasenia'],
                    status=user_data['status'],
                    imagen=user_data['imagen'],
                    tipo_usuario_id=user_data['Tipo_usuario_id'],
                    direccion=user_data['direccion'],
                    tipo_cliente=user_data['tipo_cliente'],
                    peso=user_data['peso'],
                    altura=user_data['altura'],
                    fecha_pago=user_data['fecha_pago'],
                    fecha_registro=user_data['fecha_registro']
                )
            return None
        finally:
            cur.close()