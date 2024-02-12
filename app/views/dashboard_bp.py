from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models.transaction_model import Transaction 
from app.models.savings_model import SavingGoal 
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard_bp', __name__, url_prefix='/dashboard')

# Display net cash flow of time range
def calculate_net_cash_flow(user_id, start_date, end_date):
    total_income = db.session.query(func.sum(Transaction.amount))\
                    .filter(Transaction.user_id == user_id, Transaction.type == 'income', Transaction.date >= start_date, Transaction.date < end_date)\
                    .scalar() or 0
    total_expenses = db.session.query(func.sum(Transaction.amount))\
                      .filter(Transaction.user_id == user_id, Transaction.type == 'expense', Transaction.date >= start_date, Transaction.date < end_date)\
                      .scalar() or 0
    return total_income, total_expenses, total_income - total_expenses

# Helper function for setting time ranges
def get_time_range_dates(range_type):
    today = datetime.today()
    if range_type == 'this_year':
        start_date = datetime(today.year, 1, 1)
        end_date = datetime(today.year + 1, 1, 1)
    elif range_type == 'this_month':
        start_date = datetime(today.year, today.month, 1)
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        end_date = datetime(next_year, next_month, 1)
    elif range_type == 'this_week':
        # Adjust to make Sunday the start of the week
        start_date = today - timedelta(days=(today.weekday() + 1) % 7)
        end_date = start_date + timedelta(days=6)  # End on Saturday
        end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)  # Ensure the end date covers the entire day
    elif range_type == 'today':
        start_date = datetime(today.year, today.month, today.day)
        end_date = start_date + timedelta(days=1)
    else:  # Default to 'this_month' 
        start_date = datetime(today.year, today.month, 1)
        next_month = today.month + 1 if today.month < 12 else 1
        next_year = today.year if today.month < 12 else today.year + 1
        end_date = datetime(next_year, next_month, 1)
    return start_date, end_date

# Display transaction overview
def get_transactions_overview(user_id, range_type='this_month'):
    start_date, end_date = get_time_range_dates(range_type)
    
    # Query for positive (income) and negative (expense) transactions separately
    positive_transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.type == 'income',
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).order_by(Transaction.date.desc()).all()

    negative_transactions = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.type == 'expense',
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).order_by(Transaction.date.desc()).all()

    return positive_transactions, negative_transactions

# Display saving goal progress
def get_saving_goals_progress(user_id):
    saving_goals = SavingGoal.query.filter_by(user_id=user_id).all()
    saving_goals_progress = []

    for goal in saving_goals:
        if goal.target_amount > 0:  # To avoid division by zero
            progress_percentage = (goal.current_amount / goal.target_amount) * 100
        else:
            progress_percentage = 0

        # Calculate days left for the goal
        days_left = (goal.target_date - datetime.utcnow()).days

        # Suggest next steps based on progress and time remaining
        if days_left > 0:
            daily_saving_needed = (goal.target_amount - goal.current_amount) / days_left
            suggestion = f"Save ${daily_saving_needed:.2f} daily to meet your goal."
        else:
            suggestion = "Goal deadline has passed."

        saving_goals_progress.append({
            'goal_name': goal.goal_name,
            'progress_percentage': min(progress_percentage, 100),  # Cap at 100%
            'current_amount': goal.current_amount,
            'target_amount': goal.target_amount,
            'days_left': days_left,
            'suggestion': suggestion
        })

    return saving_goals_progress

def get_financial_insights(user_id, range_type='this_month'):
    start_date, end_date = get_time_range_dates(range_type)
    
    # Aggregate expenses by category
    spending_by_category = db.session.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'expense',
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).group_by(
        Transaction.category
    ).all()

    # Aggregate income by source
    income_by_source = db.session.query(
        Transaction.category, func.sum(Transaction.amount)
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == 'income',
        Transaction.date >= start_date,
        Transaction.date < end_date
    ).group_by(
        Transaction.category
    ).all()

    return spending_by_category, income_by_source


@dashboard_bp.route('/')
@login_required
def dashboard():
    # Retrieve the time range from query parameters or default to 'this_month'
    range_type = request.args.get('range', 'this_month')

    # Calculate net cash flow using the helper function for the selected range
    start_date, end_date = get_time_range_dates(range_type)
    total_income, total_expenses, net_cash_flow = calculate_net_cash_flow(current_user.id, start_date, end_date)

    # Default fetch transactions for the selected time range
    positive_transactions, negative_transactions = get_transactions_overview(current_user.id, range_type)

    # Fetch saving goals progress
    saving_goals_progress = get_saving_goals_progress(current_user.id)

    # Get financial insights for the selected time range
    spending_by_category, income_by_source = get_financial_insights(current_user.id, range_type)

    return render_template('dashboard.html', 
                           range_type=range_type,
                           total_income=total_income, 
                           total_expenses=total_expenses, 
                           net_cash_flow=net_cash_flow, 
                           positive_transactions=positive_transactions, 
                           negative_transactions=negative_transactions,
                           saving_goals_progress=saving_goals_progress,
                           spending_by_category=spending_by_category, 
                           income_by_source=income_by_source)

