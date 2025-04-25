from app.extensions import db
from datetime import datetime

class HistorialMedida(db.Model):
    __tablename__ = 'historial_medidas_metas'
    
    id = db.Column(db.Integer, primary_key=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('metas.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    medida = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text, nullable=True)
    
    # Relación con Meta
    meta = db.relationship('Meta', back_populates='historial_medidas')
    
    def __repr__(self):
        return f"<HistorialMedida {self.id} - {self.medida} - {self.fecha}>"
    
    @property
    def to_dict(self):
        return {
            'id': self.id,
            'meta_id': self.meta_id,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M'),
            'medida': self.medida,
            'notas': self.notas
        }

class HistorialMedidas(db.Model):
    __tablename__ = 'historial_medidas'
    
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    peso = db.Column(db.Float)
    altura = db.Column(db.Float)
    imc = db.Column(db.Float)
    fecha_medicion = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # Relación
    cliente = db.relationship('Cliente', back_populates='historiales')

    # Relaciones
    fecha = db.Column(db.Date, nullable=False)
    cintura = db.Column(db.Float)
    cadera = db.Column(db.Float)
    pecho = db.Column(db.Float)
    brazos = db.Column(db.Float)
    piernas = db.Column(db.Float)
    grasa_corporal = db.Column(db.Float)
    masa_muscular = db.Column(db.Float)
    notas = db.Column(db.Text) 