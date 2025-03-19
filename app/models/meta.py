from app.extensions import db
from datetime import datetime

class Meta(db.Model):
    __tablename__ = 'metas'
    
    id = db.Column(db.Integer, primary_key=True)
    rutina_id = db.Column(db.Integer, db.ForeignKey('rutinas.id', ondelete='CASCADE'), nullable=False)
    tipo_medida = db.Column(db.String(50), nullable=False)  # brazo, pecho, peso, porcentaje_grasa, etc.
    medida_inicial = db.Column(db.Float, nullable=False)
    medida_objetivo = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)  # cm, kg, %, etc.
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_logro = db.Column(db.DateTime, nullable=True)  # Fecha en que se logró el objetivo
    logrado = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text, nullable=True)
    
    # Relación con la rutina
    rutina = db.relationship('Rutina', backref=db.backref('metas', cascade='all, delete-orphan'))
    
    # Historial de mediciones para seguimiento
    historial = db.relationship('HistorialMedida', backref='meta', cascade='all, delete-orphan')

class HistorialMedida(db.Model):
    __tablename__ = 'historial_medidas'
    
    id = db.Column(db.Integer, primary_key=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('metas.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    medida = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text, nullable=True) 