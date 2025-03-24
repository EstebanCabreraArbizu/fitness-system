from flask import Blueprint, render_template, request, flash, redirect, jsonify
from flask_login import current_user
from werkzeug.utils import secure_filename
from app.db import mysql
import os
import time

dieta = Blueprint('dieta', __name__, template_folder='app/templates')

@dieta.route('/dieta', methods=['GET', 'POST'])
def dieta_page():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('No file part')