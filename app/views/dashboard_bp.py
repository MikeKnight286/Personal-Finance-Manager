from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.transaction_model import Transaction 

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    # Defining the start and end of the current month
    today = datetime.today()
    first_day_of_month = datetime(today.year, today.month, 1)
    next_month = today.month + 1 if today.month < 12 else 1
    next_year = today.year if today.month < 12 else today.year + 1
    first_day_of_next_month = datetime(next_year, next_month, 1)
    
    # Calculate total income and expenses for the current month
    total_income = db.session.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user.id, Transaction.type == 'income', Transaction.date >= first_day_of_month, Transaction.date < first_day_of_next_month).scalar() or 0
    total_expenses = db.session.query(func.sum(Transaction.amount)).filter(Transaction.user_id == current_user.id, Transaction.type == 'expense', Transaction.date >= first_day_of_month, Transaction.date < first_day_of_next_month).scalar() or 0

    # Calculate net cash flow
    net_cash_flow = total_income - total_expenses

    return render_template('dashboard.html', total_income=total_income, total_expenses=total_expenses, net_cash_flow=net_cash_flow)
