from app import create_app
from app.extensions import db, migrate
from flask_migrate import stamp
from alembic.config import Config
from alembic import command

app = create_app()

with app.app_context():
    # Marca el estado actual de la base de datos como migrado
    # sin realizar cambios
    try:
        stamp()
        print("Base de datos marcada exitosamente con sello de migración.")
    except Exception as e:
        print(f"Error al sellar la base de datos: {e}") 