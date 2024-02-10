from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    return render_template('dashboard.html')
