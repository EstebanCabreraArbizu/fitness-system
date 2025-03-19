from app.extensions import db

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    celular = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    contrasenia = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(150), nullable=False)
    tipo_cliente = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(255), nullable=True)
    fecha_pago = db.Column(db.Date, nullable=True)
    
    # Relaciones simples sin back_populates/backref
    disciplines = db.relationship('Discipline', secondary='discipline_cliente')
    instructors = db.relationship('Instructor', secondary='cliente_instructor',
                               viewonly=True)
    # No es necesario definir 'rutinas' aquí ya que está como backref en el modelo Rutina
