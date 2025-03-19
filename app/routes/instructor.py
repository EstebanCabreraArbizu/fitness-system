from flask import Blueprint

bp = Blueprint('instructor', __name__, url_prefix='/instructor')

@bp.route('/')
def index():
    return "Panel de instructor"
