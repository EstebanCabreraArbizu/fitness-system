from app.extensions import db
from datetime import datetime
from .associations import comida_dieta
from .comida import Comida

class Dieta(db.Model):
    __tablename__ = 'dietas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    calorias_diarias = db.Column(db.Integer)
    proteinas = db.Column(db.Float)
    carbohidratos = db.Column(db.Float)
    grasas = db.Column(db.Float)
    notas = db.Column(db.Text)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    
    # Relaciones
    cliente = db.relationship('Cliente', back_populates='dietas')
    # La relación con instructor se maneja a través del backref en el modelo Instructor
    comidas = db.relationship(Comida, secondary=comida_dieta, back_populates='dietas')
    detalles_comidas = db.relationship('ComidaDieta', back_populates='dieta', cascade='all, delete-orphan')

class ComidaDieta(db.Model):
    __tablename__ = 'comidas_dieta'
    
    id = db.Column(db.Integer, primary_key=True)
    dieta_id = db.Column(db.Integer, db.ForeignKey('dietas.id', ondelete='CASCADE'), nullable=False)
    tipo_comida = db.Column(db.String(50), nullable=False)  # desayuno, almuerzo, merienda, cena
    hora = db.Column(db.Time, nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    calorias = db.Column(db.Integer)
    proteinas = db.Column(db.Float)  # en gramos
    carbohidratos = db.Column(db.Float)  # en gramos
    grasas = db.Column(db.Float)  # en gramos
    lunes = db.Column(db.Boolean, default=True)
    martes = db.Column(db.Boolean, default=True)
    miercoles = db.Column(db.Boolean, default=True)
    jueves = db.Column(db.Boolean, default=True)
    viernes = db.Column(db.Boolean, default=True)
    sabado = db.Column(db.Boolean, default=True)
    domingo = db.Column(db.Boolean, default=True)
    
    # Relación
    dieta = db.relationship('Dieta', back_populates='detalles_comidas') 