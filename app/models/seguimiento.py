from app.extensions import db
from datetime import datetime

class Seguimiento(db.Model):
    __tablename__ = 'seguimientos'
    
    id = db.Column(db.Integer, primary_key=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('metas.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    valor_actual = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text)
    
    # Relación con Meta
    meta = db.relationship('Meta', back_populates='seguimientos')
    
    @property
    def progreso(self):
        """Calcula el progreso en porcentaje"""
        if not self.meta:
            return 0
            
        if self.meta.medida_inicial == self.meta.medida_objetivo:
            return 100 if self.meta.logrado else 0
            
        progreso = ((self.valor_actual - self.meta.medida_inicial) / 
                   (self.meta.medida_objetivo - self.meta.medida_inicial)) * 100
        return min(max(0, progreso), 100)  # Asegura que el valor esté entre 0 y 100
    
    @property
    def progreso_absoluto(self):
        """Retorna el valor absoluto del progreso"""
        return abs(self.progreso) 