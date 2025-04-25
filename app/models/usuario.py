# Relaciones
clientes = db.relationship('Cliente', back_populates='usuario', cascade='all, delete-orphan')
horarios_asignados = db.relationship('Horario', back_populates='instructor') 