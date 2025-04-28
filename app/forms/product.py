from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, DateField, FileField, MultipleFileField, BooleanField
from wtforms.validators import DataRequired, Optional, NumberRange

class ProductForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired()])
    category = IntegerField('Categoría', validators=[DataRequired()])
    description = TextAreaField('Descripción', validators=[DataRequired()])
    marca = StringField('Marca', validators=[DataRequired()])
    purchase_price = DecimalField('Precio de Compra', validators=[DataRequired(), NumberRange(min=0)])
    price = DecimalField('Precio de Venta', validators=[DataRequired(), NumberRange(min=0)])
    descuento = DecimalField('Descuento', validators=[Optional(), NumberRange(min=0)])
    palabras_claves = TextAreaField('Palabras Claves', validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[Optional()])
    fecha_fin = DateField('Fecha de Fin', validators=[Optional()])
    images = MultipleFileField('Imágenes del Producto')
    relevant = BooleanField('Relevante')
    additional = BooleanField('Adicional')
    outstanding = BooleanField('Destacado') 