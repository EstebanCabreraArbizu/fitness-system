from app.extensions import db

class Discipline(db.Model):
    __tablename__ = 'discipline'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    
    # Relaciones
    instructores = db.relationship('Instructor', secondary='discipline_instructor')
    clientes = db.relationship('Cliente', secondary='discipline_cliente')
    
    def __repr__(self):
        return f"<Discipline {self.nombre}>"
