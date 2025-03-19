from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from app.extensions import db, migrate, login_manager
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crear directorio de uploads si no existe
    upload_folder = app.config.get('UPLOAD_FOLDER', os.path.join(app.root_path, 'static', 'uploads'))
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Inicializar extensiones
    db.init_app(app)
    
    # Configurar migrate con opciones especiales
    migrate.init_app(app, db, compare_type=True, render_as_batch=True, include_schemas=True)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.instructor import Instructor
        return Instructor.query.get(int(user_id))

    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.client import client_bp
    from app.routes.rutina import rutina_bp
    from app.routes.meta import meta_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(rutina_bp)
    app.register_blueprint(meta_bp)

    # Ruta raíz
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('client.index'))
        return redirect(url_for('auth.login'))

    return app
