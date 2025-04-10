from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.disciplina import Disciplina
from app.extensions import db

bp = Blueprint('disciplina', __name__)

@bp.route('/disciplinas')
def lista_disciplinas():
    disciplinas = Disciplina.query.all()
    return render_template('disciplina/lista.html', disciplinas=disciplinas)

@bp.route('/disciplinas/crear', methods=['GET', 'POST'])
def crear_disciplina():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        
        disciplina = Disciplina(nombre=nombre, descripcion=descripcion)
        db.session.add(disciplina)
        db.session.commit()
        
        flash('Disciplina creada exitosamente', 'success')
        return redirect(url_for('disciplina.lista_disciplinas'))
        
    return render_template('disciplina/crear.html')

@bp.route('/disciplinas/<int:id>/editar', methods=['GET', 'POST'])
def editar_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    
    if request.method == 'POST':
        disciplina.nombre = request.form.get('nombre')
        disciplina.descripcion = request.form.get('descripcion')
        
        db.session.commit()
        flash('Disciplina actualizada exitosamente', 'success')
        return redirect(url_for('disciplina.lista_disciplinas'))
        
    return render_template('disciplina/editar.html', disciplina=disciplina)

@bp.route('/disciplinas/<int:id>/eliminar', methods=['POST'])
def eliminar_disciplina(id):
    disciplina = Disciplina.query.get_or_404(id)
    db.session.delete(disciplina)
    db.session.commit()
    
    flash('Disciplina eliminada exitosamente', 'success')
    return redirect(url_for('disciplina.lista_disciplinas')) 