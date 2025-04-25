from app.extensions import db
from datetime import datetime

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    horario_id = db.Column(db.Integer, db.ForeignKey('horarios_servicio.id', ondelete='CASCADE'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha_reserva = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente, confirmada, cancelada, completada
    notas = db.Column(db.Text)
    
    # Relaciones
    horario = db.relationship('HorarioServicio', back_populates='reservas')
    cliente = db.relationship('Cliente', back_populates='reservas')
    
    def __repr__(self):
        return f"<Reserva {self.id} - {self.estado}>"
    
    @property
    def estado_texto(self):
        estados = {
            'pendiente': 'Pendiente',
            'confirmada': 'Confirmada',
            'cancelada': 'Cancelada',
            'completada': 'Completada'
        }
        return estados.get(self.estado, self.estado)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'horario_id': self.horario_id,
            'cliente_id': self.cliente_id,
            'fecha_reserva': self.fecha_reserva.strftime('%Y-%m-%d %H:%M'),
            'estado': self.estado_texto,
            'notas': self.notas
        } 