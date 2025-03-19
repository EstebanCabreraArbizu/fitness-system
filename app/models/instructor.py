from app.extensions import db
from flask_login import UserMixin

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
    
    # Solo mantén las relaciones esenciales - evita back_populates/backref
    disciplines = db.relationship('Discipline', secondary='discipline_instructor')
    clientes = db.relationship('Cliente', secondary='cliente_instructor', viewonly=True)
    rutinas = db.relationship('Rutina', backref='instructor', foreign_keys='Rutina.instructor_id')

    def get_id(self):
        return str(self.id)
