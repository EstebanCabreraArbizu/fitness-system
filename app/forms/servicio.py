from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, BooleanField, FieldList, FormField, FileField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email, Optional

class HorarioForm(FlaskForm):
    dia_semana = IntegerField('Día de la Semana', validators=[
        DataRequired(message="Seleccione un día de la semana"),
        NumberRange(min=0, max=6, message="Día inválido")
    ])
    hora_inicio = StringField('Hora Inicio', validators=[
        DataRequired(message="La hora de inicio es requerida")
    ])
    hora_fin = StringField('Hora Fin', validators=[
        DataRequired(message="La hora de fin es requerida")
    ])

class ServicioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es requerido"),
        Length(min=3, max=100, message="El nombre debe tener entre 3 y 100 caracteres")
    ])
    
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(message="La descripción es requerida"),
        Length(min=10, max=500, message="La descripción debe tener entre 10 y 500 caracteres")
    ])
    
    precio = DecimalField('Precio', validators=[
        DataRequired(message="El precio es requerido"),
        NumberRange(min=0, message="El precio no puede ser negativo")
    ])
    
    duracion = IntegerField('Duración (minutos)', validators=[
        DataRequired(message="La duración es requerida"),
        NumberRange(min=15, max=240, message="La duración debe estar entre 15 y 240 minutos")
    ])
    
    capacidad_maxima = IntegerField('Capacidad Máxima', validators=[
        DataRequired(message="La capacidad máxima es requerida"),
        NumberRange(min=1, max=50, message="La capacidad debe estar entre 1 y 50 personas")
    ])
    
    horarios = FieldList(FormField(HorarioForm), min_entries=1)
    activo = BooleanField('Activo', default=True)

class EditarPerfilInstructorForm(FlaskForm):
    nombres = StringField('Nombres', validators=[DataRequired(), Length(max=100)])
    apellidos = StringField('Apellidos', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    telefono = StringField('Teléfono', validators=[Optional(), Length(max=20)])
    edad = IntegerField('Edad', validators=[Optional(), NumberRange(min=16, max=100)])
    estudios = TextAreaField('Estudios', validators=[Optional(), Length(max=500)])
    imagen = FileField('Foto de Perfil (opcional)')
    submit = SubmitField('Guardar Cambios')

class FotoInstructorForm(FlaskForm):
    imagen = FileField('Foto con Estudiantes', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Subir Foto') 