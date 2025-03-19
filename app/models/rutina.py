from app.extensions import db
from datetime import datetime

class Rutina(db.Model):
    __tablename__ = 'rutinas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'), nullable=False)
    discipline_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)
    nivel = db.Column(db.String(20), nullable=False)  # principiante, intermedio, avanzado
    status = db.Column(db.Integer, default=1, nullable=False)
    
    # Relaciones simplificadas
    discipline = db.relationship('Discipline')
    cliente = db.relationship('Cliente', backref='rutinas')
    
    ejercicios = db.relationship('EjercicioRutina', cascade='all, delete-orphan')

class EjercicioRutina(db.Model):
    __tablename__ = 'ejercicios_rutina'
    
    id = db.Column(db.Integer, primary_key=True)
    rutina_id = db.Column(db.Integer, db.ForeignKey('rutinas.id', ondelete='CASCADE'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    series = db.Column(db.Integer, nullable=False)
    repeticiones = db.Column(db.Integer, nullable=False)
    descanso = db.Column(db.Integer, nullable=False)  # en segundos
    dia_semana = db.Column(db.Integer, nullable=False)  # 1-7 para representar días
    orden = db.Column(db.Integer, nullable=False)
    notas = db.Column(db.Text) 