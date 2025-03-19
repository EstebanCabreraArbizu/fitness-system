import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    # Configuración básica
    SECRET_KEY = os.environ.get('SECRET_KEY', 'una_clave_secreta_muy_segura')
    
    # Configuración de la base de datos
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:marte@localhost/personal_trainer_db2'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración para subida de archivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max-limit