# app/__init__.py
from flask import Flask, current_app
from datetime import timedelta
from app.db import init_db, get_db
from dotenv import load_dotenv
import os
# Create Flask app
app = Flask(__name__)
app.secret_key = "mysecretkey"

# Load environment variables
load_dotenv()

# Configure app before initializing extensions
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7)
app.config['SESSION_PROTECTION'] = 'strong'
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER') or 'root'
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD') or 'password'
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST') or '127.0.0.1'
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB') or 'flaskcrud'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

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

@login_manager.user_loader
def load_user(user_id):
    """Carga el usuario desde la sesión."""
    if not user_id:
        return None
        
    try:
        # Extract the type prefix (c_ or i_) and the actual ID
        if user_id.startswith('c_'):
            real_id = user_id[2:]  # Remove 'c_' prefix
            return load_client(real_id)
        elif user_id.startswith('i_'):
            real_id = user_id[2:]  # Remove 'i_' prefix
            return load_instructor(real_id)
        else:
            return None
    except Exception as e:
        current_app.logger.error(f"Error in load_user: {str(e)}")
        return None

def load_client(user_id):
    """Carga un cliente desde la base de datos."""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Cliente WHERE id = %s AND status = 1
        """, (user_id,))
        data = cursor.fetchone()
        cursor.close()
        
        # Filter out fecha_registro if present but not in __init__
        if data and 'fecha_registro' in data and Client.__init__.__code__.co_varnames.count('fecha_registro') == 0:
            data.pop('fecha_registro')
            
        return Client(**data) if data else None
    except Exception as e:
        current_app.logger.error(f"Error loading client: {str(e)}")
        return None

def load_instructor(user_id):
    """Carga un instructor desde la base de datos."""
    try:
        conn = get_db(current_app)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombres, celular, email, contrasenia, status, apellidos, imagen
            FROM Instructor WHERE id = %s AND status = 1
        """, (user_id,))
        data = cursor.fetchone()
        cursor.close()
        
        return Instructor(**data) if data else None
    except Exception as e:
        current_app.logger.error(f"Error loading instructor: {str(e)}")
        return None

# Import routes after app initialization
from app.routes.users import users
from app.routes.products import products
from app.routes.dieta import dieta
# Register blueprints
app.register_blueprint(users)
app.register_blueprint(products, url_prefix='/products')
app.register_blueprint(dieta, url_prefix='/dietas')