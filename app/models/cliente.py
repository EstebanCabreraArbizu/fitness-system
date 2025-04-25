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
    
    # Relaciones
    disciplines = db.relationship('Discipline', secondary='discipline_cliente', back_populates='clientes')
    instructors = db.relationship('Instructor', secondary='cliente_instructor', viewonly=True)
    testimonios = db.relationship('Testimonio', back_populates='cliente', cascade='all, delete-orphan')
    reservas = db.relationship('Reserva', back_populates='cliente', cascade='all, delete-orphan')
    historiales = db.relationship('HistorialMedidas', back_populates='cliente', cascade='all, delete-orphan')
    
    def __init__(self, nombres, apellidos, email, celular=None):
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.celular = celular

    # Relación con dietas
    dietas = db.relationship('Dieta', back_populates='cliente', cascade='all, delete-orphan')
    
    # Relación con mediciones
    mediciones = db.relationship('Medicion', back_populates='cliente', cascade='all, delete-orphan',
                               order_by='Medicion.fecha.desc()')