from app.extensions import db
from app.models.instructor import Instructor
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    category = db.Column(db.Integer)
    description = db.Column(db.Text)
    marca = db.Column(db.String(100), nullable=False)
    purchase_price = db.Column(db.Numeric(10, 2))
    price = db.Column(db.Numeric(10, 2))
    descuento = db.Column(db.Numeric(10, 2))
    previous_price = db.Column(db.Numeric(10, 2))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    status = db.Column(db.Integer, nullable=False, default=1)
    relevant = db.Column(db.Integer, nullable=False, default=0)
    additional = db.Column(db.String(200))
    outstanding = db.Column(db.Integer, nullable=False, default=1)
    palabras_claves = db.Column(db.Text, nullable=False)
    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)
    profesor = db.Column(db.String(100), nullable=False)
    profesor_foto = db.Column(db.String(100), nullable=False)

    # Relaciones
    images = db.relationship('ProductImage', back_populates='product', cascade='all, delete-orphan')
    instructor = db.relationship('Instructor', back_populates='products')

    def __repr__(self):
        return f'<Product {self.title}>'

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    
    id = db.Column(db.Integer, primary_key=True)
    image_name = db.Column(db.Text, nullable=False)
    color_id = db.Column(db.Integer, nullable=False, default=1)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    # Relaciones
    product = db.relationship('Product', back_populates='images')

    def __repr__(self):
        return f'<ProductImage {self.image_name}>'
