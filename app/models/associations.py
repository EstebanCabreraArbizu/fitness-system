from app.extensions import db

# Definir tablas de asociación correctamente (sin declaraciones redundantes)
discipline_cliente = db.Table('discipline_cliente',
    db.Column('discipline_id', db.Integer, db.ForeignKey('discipline.id'), primary_key=True),
    db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id'), primary_key=True)
)

cliente_instructor = db.Table('cliente_instructor',
    db.Column('cliente_id', db.Integer, db.ForeignKey('cliente.id'), primary_key=True),
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'), primary_key=True)
)

discipline_instructor = db.Table('discipline_instructor',
    db.Column('discipline_id', db.Integer, db.ForeignKey('discipline.id'), primary_key=True),
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'), primary_key=True)
)

instructor_products = db.Table('instructor_products',
    db.Column('instructor_id', db.Integer, db.ForeignKey('instructor.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
) 