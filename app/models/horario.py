from app.extensions import db
from datetime import datetime, time

class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    servicio_id = db.Column(db.Integer, db.ForeignKey('servicios.id'), nullable=False)
    dia_semana = db.Column(db.Integer, nullable=False)  # 0=Lunes, 1=Martes, etc.
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    cupo_maximo = db.Column(db.Integer, nullable=False, default=1)
    activo = db.Column(db.Boolean, default=True)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    servicio = db.relationship('Servicio', back_populates='horarios')
    reservas = db.relationship('Reserva', back_populates='horario', cascade='all, delete-orphan')

    def __init__(self, servicio_id, dia_semana, hora_inicio, hora_fin, cupo_maximo):
        self.servicio_id = servicio_id
        self.dia_semana = dia_semana
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.cupo_maximo = cupo_maximo
        self.activo = True

    @property
    def dia_semana_texto(self):
        dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        return dias[self.dia_semana]

    @property
    def horario_texto(self):
        return f"{self.hora_inicio.strftime('%H:%M')} - {self.hora_fin.strftime('%H:%M')}"

    @property
    def disponibilidad(self):
        return self.cupo_maximo - len(self.reservas)

    def tiene_cupo(self):
        return self.disponibilidad > 0

    def esta_disponible(self, fecha):
        """Verifica si el horario está disponible para una fecha específica"""
        # Verificar que sea el día de la semana correcto
        if fecha.weekday() != self.dia_semana:
            return False
            
        # Verificar que tenga cupo disponible
        if not self.tiene_cupo():
            return False
            
        # Verificar que el horario esté activo
        if not self.activo:
            return False
            
        return True

    def __repr__(self):
        return f"<Horario {self.dia_semana_texto} {self.horario_texto}>"

    @property
    def cupos_disponibles(self):
        """Calcula los cupos disponibles para este horario"""
        from app.models import Reserva
        reservas_activas = Reserva.query.filter_by(
            horario_id=self.id,
            estado='confirmada'
        ).count()
        return max(0, self.cupo_maximo - reservas_activas)

    @property
    def esta_lleno(self):
        """Verifica si el horario está lleno"""
        return self.cupos_disponibles == 0

    def verificar_disponibilidad(self, fecha):
        """Verifica si hay cupo disponible para una fecha específica"""
        from app.models import Reserva
        reservas_fecha = Reserva.query.filter_by(
            horario_id=self.id,
            fecha=fecha,
            estado='confirmada'
        ).count()
        return reservas_fecha < self.cupo_maximo

    def obtener_reservas_fecha(self, fecha):
        """Obtiene las reservas para una fecha específica"""
        from app.models import Reserva
        return Reserva.query.filter_by(
            horario_id=self.id,
            fecha=fecha
        ).all()

    def es_horario_valido(self):
        """Verifica que la hora de fin sea posterior a la hora de inicio"""
        return self.hora_inicio < self.hora_fin

    def to_dict(self):
        """Convierte el horario a un diccionario para API/JSON"""
        return {
            'id': self.id,
            'servicio_id': self.servicio_id,
            'dia_semana': self.dia_semana,
            'hora_inicio': self.hora_inicio.strftime('%H:%M'),
            'hora_fin': self.hora_fin.strftime('%H:%M'),
            'cupo_maximo': self.cupo_maximo,
            'activo': self.activo
        } 