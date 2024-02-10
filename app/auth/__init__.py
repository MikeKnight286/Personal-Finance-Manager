from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import auth_views  # Import auth_views to register routes with the Blueprint
