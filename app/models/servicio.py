from app.extensions import db
from datetime import datetime

class Servicio(db.Model):
    __tablename__ = 'servicios'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)  # duración en minutos
    capacidad_maxima = db.Column(db.Integer, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    instructor = db.relationship('Instructor', back_populates='servicios')
    horarios = db.relationship('HorarioServicio', back_populates='servicio', cascade='all, delete-orphan')
    
    def __init__(self, nombre, descripcion, precio, duracion, instructor_id):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.duracion = duracion
        self.instructor_id = instructor_id
        self.activo = True
    
    def __repr__(self):
        return f"<Servicio {self.nombre}>"
    
    @property
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'duracion': self.duracion,
            'instructor_id': self.instructor_id,
            'activo': self.activo
        }
    
    @property
    def precio_formateado(self):
        return f"${self.precio:,.2f}"
    
    @property
    def duracion_formateada(self):
        horas = self.duracion // 60
        minutos = self.duracion % 60
        if horas > 0:
            return f"{horas}h {minutos}min" if minutos > 0 else f"{horas}h"
        return f"{minutos}min"

class Certificacion(db.Model):
    __tablename__ = 'certificaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    institucion = db.Column(db.String(200), nullable=False)
    fecha_obtencion = db.Column(db.Date)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(255))  # ruta a la imagen del certificado
    
    # Relación
    instructor = db.relationship('Instructor', back_populates='certificaciones')

class Testimonio(db.Model):
    __tablename__ = 'testimonios'
    
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    contenido = db.Column(db.Text, nullable=False)
    calificacion = db.Column(db.Integer)  # 1-5 estrellas
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    imagen_antes = db.Column(db.String(255))  # ruta a la imagen "antes"
    imagen_despues = db.Column(db.String(255))  # ruta a la imagen "después"
    
    # Relaciones
    instructor = db.relationship('Instructor', back_populates='testimonios')
    cliente = db.relationship('Cliente', back_populates='testimonios')

class HorarioServicio(db.Model):
    __tablename__ = 'horarios_servicio'
    
    id = db.Column(db.Integer, primary_key=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Lunes, 6=Domingo
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    cupo_maximo = db.Column(db.Integer, default=1)
    activo = db.Column(db.Boolean, default=True)
    
    # Relaciones
    servicio = db.relationship('Servicio', back_populates='horarios')
    reservas = db.relationship('Reserva', back_populates='horario', cascade='all, delete-orphan')
    
    def __repr__(self):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return f"<Horario {dias[self.dia_semana]} {self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}>"
    
    @property
    def dia_texto(self):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dias[self.dia_semana]
    
    @property
    def horario_texto(self):
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"
    
    @property
    def disponibilidad(self):
        return self.cupo_maximo - len(self.reservas)
    
    def tiene_cupo(self):
        return self.disponibilidad > 0
    
    def esta_disponible(self):
        return self.activo and self.tiene_cupo() 