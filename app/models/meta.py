from app.extensions import db
from datetime import datetime

class Meta(db.Model):
    __tablename__ = 'metas'
    
    id = db.Column(db.Integer, primary_key=True)
    rutina_id = db.Column(db.Integer, db.ForeignKey('rutinas.id', ondelete='CASCADE'), nullable=False)
    tipo_medida = db.Column(db.String(50), nullable=False)
    medida_inicial = db.Column(db.Float, nullable=False)
    medida_objetivo = db.Column(db.Float, nullable=False)
    unidad = db.Column(db.String(20), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_logro = db.Column(db.DateTime, nullable=True)
    logrado = db.Column(db.Boolean, default=False)
    notas = db.Column(db.Text)
    
    # Relaciones
    rutina = db.relationship('Rutina', back_populates='metas')
    seguimientos = db.relationship('Seguimiento', 
                                back_populates='meta',
                                cascade='all, delete-orphan',
                                order_by='Seguimiento.fecha.desc()')
    historial_medidas = db.relationship('HistorialMedida', 
                                backref='meta',
                                cascade='all, delete-orphan',
                                order_by='HistorialMedida.fecha.asc()')
    
    @property
    def valor_actual(self):
        """Obtiene el valor actual basado en el último seguimiento"""
        if not self.seguimientos:
            return self.medida_inicial
        return self.seguimientos[0].valor_actual if self.seguimientos else self.medida_inicial
    
    @property
    def progreso(self):
        """Calcula el progreso hacia la meta en porcentaje"""
        if self.medida_inicial == self.medida_objetivo:
            return 100 if self.logrado else 0
            
        progreso = ((self.valor_actual - self.medida_inicial) / 
                   (self.medida_objetivo - self.medida_inicial)) * 100
        return min(max(0, progreso), 100)  # Asegura que el valor esté entre 0 y 100
    
    def actualizar_progreso(self, nuevo_valor):
        """Actualiza el progreso creando un nuevo seguimiento"""
        from app.models.seguimiento import Seguimiento
        
        seguimiento = Seguimiento(
            meta_id=self.id,
            valor_actual=nuevo_valor
        )
        db.session.add(seguimiento)
        
        if self.progreso >= 100 and not self.logrado:
            self.logrado = True
            self.fecha_logro = datetime.utcnow()
            
        return seguimiento

class HistorialMedida(db.Model):
    __tablename__ = 'historial_medidas_metas'
    
    id = db.Column(db.Integer, primary_key=True)
    meta_id = db.Column(db.Integer, db.ForeignKey('metas.id', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    medida = db.Column(db.Float, nullable=False)
    notas = db.Column(db.Text, nullable=True) 