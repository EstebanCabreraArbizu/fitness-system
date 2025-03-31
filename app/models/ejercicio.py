from app.extensions import db
from .associations import ejercicio_rutina

class Ejercicio(db.Model):
    __tablename__ = 'ejercicios'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    video_url = db.Column(db.String(255))
    imagen_url = db.Column(db.String(255))
    categoria = db.Column(db.String(50))  # cardio, fuerza, flexibilidad, etc.
    equipamiento = db.Column(db.String(100))
    musculos_trabajados = db.Column(db.String(200))
    nivel_dificultad = db.Column(db.String(20))
    
    # Relaciones
    rutinas = db.relationship('Rutina', secondary=ejercicio_rutina, back_populates='ejercicios') 