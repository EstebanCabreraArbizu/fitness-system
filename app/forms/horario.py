from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TimeField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, ValidationError
from datetime import datetime, timedelta

class HorarioForm(FlaskForm):
    dias_semana = SelectMultipleField('Días de la Semana', 
                           choices=[(str(i), dia) for i, dia in enumerate(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'])],
                           validators=[DataRequired()])
    hora_inicio = TimeField('Hora de Inicio', validators=[DataRequired()])
    hora_fin = TimeField('Hora de Fin', validators=[DataRequired()])
    cupo_maximo = IntegerField('Cupo Máximo', 
                             validators=[DataRequired(), NumberRange(min=1, message='El cupo máximo debe ser al menos 1')])
    submit = SubmitField('Guardar')

    def validate_hora_fin(self, field):
        if self.hora_inicio.data and field.data:
            inicio = datetime.combine(datetime.today(), self.hora_inicio.data)
            fin = datetime.combine(datetime.today(), field.data)
            duracion = fin - inicio
            if duracion.total_seconds() > 3600:  # 3600 segundos = 1 hora
                raise ValidationError('La duración no puede exceder 60 minutos')
            if duracion.total_seconds() <= 0:
                raise ValidationError('La hora de fin debe ser posterior a la hora de inicio') 