from app.extensions import db
from .associations import comida_dieta

class Comida(db.Model):
    __tablename__ = 'comidas'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    calorias = db.Column(db.Integer)
    proteinas = db.Column(db.Float)
    carbohidratos = db.Column(db.Float)
    grasas = db.Column(db.Float)
    tipo = db.Column(db.String(50))  # desayuno, almuerzo, cena, snack
    
    # Relaciones
    dietas = db.relationship('Dieta', secondary=comida_dieta, back_populates='comidas') 