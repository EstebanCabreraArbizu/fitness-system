from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.instructor import Instructor

# Crear el Blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        instructor = Instructor.query.filter_by(email=email).first()
        
        # Ahora comparamos con contrasenia en lugar de password_hash
        if instructor and instructor.contrasenia == password:
            login_user(instructor)
            return redirect(url_for('client.index'))
        
        # O si está cifrada
        if instructor and check_password_hash(instructor.contrasenia, password):
            login_user(instructor)
            return redirect(url_for('client.index'))
        
        flash('Credenciales inválidas', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']

        if Instructor.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('auth.register'))

        nuevo_instructor = Instructor(
            email=email,
            contrasenia=generate_password_hash(password),  # Usar contrasenia aquí
            nombres=nombres,
            apellidos=apellidos,
            telefono=telefono,
            activo=True
        )

        try:
            db.session.add(nuevo_instructor)
            db.session.commit()
            flash('Registro exitoso! Por favor inicia sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Error al registrar: ' + str(e), 'error')

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
