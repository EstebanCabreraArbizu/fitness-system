# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from datetime import timedelta
from app.db import mysql, init_db  # This should be fine now that db.py doesn't import app
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

# Now import models that depend on db
from app.models.client import Client
from app.models.instructor import Instructor

# Set up login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'users.login'
login_manager.login_message = 'You need to login to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    if isinstance(user_id, str) and user_id.startswith('C'):
        client_id = user_id[1:]
        return Client.get_id(client_id)
    elif isinstance(user_id, str) and user_id.startswith('I'):
        instructor_id = user_id[1:]
        return Instructor.get_id(instructor_id)

# Import routes after app initialization
from app.routes.users import users
from app.routes.products import products

# Register blueprints
app.register_blueprint(users)
app.register_blueprint(products, url_prefix='/products')