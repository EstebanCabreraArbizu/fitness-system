from app.extensions import db

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=True)
    category = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    marca = db.Column(db.String(100), nullable=False)
    purchase_price = db.Column(db.Float(10,2), nullable=True)
    price = db.Column(db.Float(10,2), nullable=True)
    descuento = db.Column(db.Float(10,2), nullable=True)
    previous_price = db.Column(db.Float(10,2), nullable=True)
    date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, nullable=True)
    status = db.Column(db.Integer, nullable=False, default=1)
    relevant = db.Column(db.Integer, nullable=False, default=0)
    additional = db.Column(db.String(200), nullable=True)
    outstanding = db.Column(db.Integer, nullable=False, default=1)
    palabras_claves = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=True)
    fecha_fin = db.Column(db.Date, nullable=True)
    profesor = db.Column(db.String(100), nullable=False)
    profesor_foto = db.Column(db.String(100), nullable=False)

    # Relación con las imágenes
    images = db.relationship('ProductImage', backref='product', lazy=True)
