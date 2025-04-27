from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Instructor(UserMixin, db.Model):
    __tablename__ = 'instructor'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contrasenia = db.Column(db.String(255), nullable=False)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    activo = db.Column(db.Boolean, default=True)
    fecha_registro = db.Column(db.DateTime, default=db.func.current_timestamp())
    edad = db.Column(db.Integer)
    estudios = db.Column(db.Text)
    
    # Relaciones simplificadas
    disciplines = db.relationship('Discipline', secondary='discipline_instructor')
    clientes = db.relationship('Cliente', secondary='cliente_instructor', viewonly=True)
    rutinas = db.relationship('Rutina', backref='instructor_ref', foreign_keys='Rutina.instructor_id')
    dietas = db.relationship('Dieta', foreign_keys='Dieta.instructor_id')
    
    # Nuevas relaciones
    servicios = db.relationship('Servicio', back_populates='instructor', cascade='all, delete-orphan')
    certificaciones = db.relationship('Certificacion', back_populates='instructor', cascade='all, delete-orphan')
    testimonios = db.relationship('Testimonio', back_populates='instructor', cascade='all, delete-orphan')
    fotos = db.relationship('FotoInstructor', back_populates='instructor', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.contrasenia = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.contrasenia, password)

    def get_id(self):
        return str(self.id)

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

class FotoInstructor(db.Model):
    __tablename__ = 'fotos_instructor'
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    ruta = db.Column(db.String(255), nullable=False)
    descripcion = db.Column(db.Text)
    instructor = db.relationship('Instructor', back_populates='fotos')
