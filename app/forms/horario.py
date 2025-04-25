from flask_wtf import FlaskForm
from wtforms import SelectField, TimeField, IntegerField, BooleanField
from wtforms.validators import DataRequired, NumberRange

class HorarioForm(FlaskForm):
    servicio = SelectField('Servicio', validators=[DataRequired()], coerce=int)
    instructor = SelectField('Instructor', validators=[DataRequired()], coerce=int)
    dia_semana = SelectField('Día de la semana', 
                           choices=[
                               (0, 'Lunes'),
                               (1, 'Martes'),
                               (2, 'Miércoles'),
                               (3, 'Jueves'),
                               (4, 'Viernes'),
                               (5, 'Sábado'),
                               (6, 'Domingo')
                           ],
                           validators=[DataRequired()],
                           coerce=int)
    hora_inicio = TimeField('Hora de inicio', validators=[DataRequired()])
    hora_fin = TimeField('Hora de fin', validators=[DataRequired()])
    cupo_maximo = IntegerField('Cupo máximo', 
                              validators=[
                                  DataRequired(),
                                  NumberRange(min=1, message="El cupo máximo debe ser al menos 1")
                              ])
    activo = BooleanField('Activo', default=True)

    def __init__(self, *args, **kwargs):
        super(HorarioForm, self).__init__(*args, **kwargs)
        from app.models import Servicio, Usuario
        # Cargar opciones de servicios
        self.servicio.choices = [(s.id, s.nombre) 
                                for s in Servicio.query.filter_by(activo=True).all()]
        # Cargar opciones de instructores (usuarios con rol de instructor)
        self.instructor.choices = [(u.id, f"{u.nombre} {u.apellido}") 
                                 for u in Usuario.query.filter_by(rol='instructor', activo=True).all()] 