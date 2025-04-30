# app/__init__.py
from flask import Flask, current_app
from datetime import timedelta
from app.db import init_db, get_db
from dotenv import load_dotenv
import os
# Create Flask app
app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')
app.secret_key = "mysecretkey"

# Load environment variables
load_dotenv()

# Configure app before initializing extensions
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['SESSION_PROTECTION'] = 'strong'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER') or 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') or 'marte'
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') or '127.0.0.1'
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') or 'flaskcrud'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER') or 'app/static/uploads'

# Initialize database
init_db(app)

# Set up login manager
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'You need to login to access this page.'
login_manager.login_message_category = 'info'

# Now import models that depend on login_manager
from app.models.client import Client
from app.models.instructor import Instructor
from app.models.user import User
# Modificar la función load_user y eliminar load_client y load_instructor

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la sesión."""
    if not user_id:
        return None
        
    try:
        # Extraer el ID real (sin prefijo)
        if user_id.startswith('u_'):
            real_id = user_id[2:]  # Remover prefijo 'u_'
            return User.get_by_id(real_id)
        else:
            return None
    except Exception as e:
        current_app.logger.error(f"Error in load_user: {str(e)}")
        return None

# Import routes after app initialization
from app.routes.users import users
from app.routes.products import products
from app.routes.dieta import dieta
from app.routes.alumnos import alumnos
from app.routes.rutinas import rutinas

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(dieta, url_prefix='/dietas')
app.register_blueprint(alumnos, url_prefix='/alumnos')
app.register_blueprint(rutinas, url_prefix='/rutinas')