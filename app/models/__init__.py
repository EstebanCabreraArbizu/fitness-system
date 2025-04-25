from .cliente import Cliente
from .instructor import Instructor
from .discipline import Discipline
from .rutina import Rutina, EjercicioRutina
from .meta import Meta
from .historial_medidas import HistorialMedida
from .medicion import Medicion
from .servicio import Servicio, HorarioServicio, Certificacion, Testimonio
from .reserva import Reserva

__all__ = [
    'Cliente',
    'Instructor',
    'Discipline',
    'Rutina',
    'EjercicioRutina',
    'Meta',
    'HistorialMedida',
    'Medicion',
    'Servicio',
    'HorarioServicio',
    'Certificacion',
    'Testimonio',
    'Reserva'
]
