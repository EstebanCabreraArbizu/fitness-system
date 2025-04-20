from app.extensions import db
from datetime import datetime

class Medicion(db.Model):
    __tablename__ = 'mediciones'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Medidas corporales
    peso = db.Column(db.Float)  # en kg
    altura = db.Column(db.Float)  # en cm
    imc = db.Column(db.Float)  # Índice de Masa Corporal
    
    # Circunferencias
    cintura = db.Column(db.Float)  # en cm
    cadera = db.Column(db.Float)  # en cm
    pecho = db.Column(db.Float)  # en cm
    brazo = db.Column(db.Float)  # en cm
    muslo = db.Column(db.Float)  # en cm
    pantorrilla = db.Column(db.Float)  # en cm
    
    # Composición corporal
    porcentaje_grasa = db.Column(db.Float)  # en %
    masa_muscular = db.Column(db.Float)  # en kg
    masa_grasa = db.Column(db.Float)  # en kg
    
    # Notas y observaciones
    notas = db.Column(db.Text)
    
    # Relación con Cliente
    cliente = db.relationship('Cliente', back_populates='mediciones')
    
    def calcular_imc(self):
        """Calcula el IMC basado en peso y altura"""
        if self.altura and self.peso:
            altura_m = self.altura / 100  # Convertir cm a m
            return round(self.peso / (altura_m ** 2), 2)
        return None 