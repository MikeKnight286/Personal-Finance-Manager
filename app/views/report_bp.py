from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db, mail
from app.models.transaction_model import Transaction
from flask_mail import Message
from datetime import datetime, time
from sqlalchemy import func
from app.models.users_model import User
from app.services.user_service import ReportPreferencesForm

report_bp = Blueprint('report_bp', __name__, url_prefix='/report')

@report_bp.route('/')
@login_required
def report():
    form = ReportPreferencesForm(obj=current_user)
    start_of_month = datetime(datetime.today().year, datetime.today().month, 1)
    today = datetime.today().date()  # Get the current date without time
    end_of_today = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)  # Set to the end of today

    # Query transactions for monthly reports
    monthly_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_of_month,
        func.date(Transaction.date) <= today  # Ensure it includes all of today
    ).all()

    # Adjusted query for daily transactions
    daily_transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        func.date(Transaction.date) == today  # Compare only the date parts
    ).all()

    return render_template('report.html', monthly_transactions=monthly_transactions, daily_transactions=daily_transactions, form=form)

def send_email(subject, recipient, html_body):
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    mail.send(msg)

def generate_report_html(transactions, report_title):
    html_body = f"<h1>{report_title}</h1><ul>"
    for transaction in transactions:
        html_body += f"<li>{transaction.date.strftime('%Y-%m-%d %I:%M %p')}: {transaction.type} - {transaction.category} - ${transaction.amount} - {transaction.description}</li>"
    html_body += "</ul>"
    return html_body

@report_bp.route('/send_report')
@login_required
def send_report():
    report_type = request.args.get('report_type', 'monthly')  # Default to 'monthly' if not specified
    
    # Common setup
    subject = f"Your {report_type.capitalize()} Transaction Report"
    recipient = current_user.email
    today = datetime.today().date()
    start_of_month = datetime(datetime.today().year, datetime.today().month, 1)
    
    if report_type == 'daily':
        transactions = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            func.date(Transaction.date) == today
        ).all()
        report_title = "Daily Transactions"
    else:  # Default to monthly report
        transactions = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= start_of_month,
            func.date(Transaction.date) <= today
        ).all()
        report_title = "Monthly Transactions"
    
    html_body = generate_report_html(transactions, report_title)

    # Send the email
    send_email(subject, recipient, html_body)
    
    flash(f"{report_title} sent successfully.")
    return redirect(url_for('report_bp.report'))

@report_bp.route('/report_preferences', methods=['GET', 'POST'])
@login_required
def report_preferences():
    form = ReportPreferencesForm(request.form, obj=current_user)

    if request.method == 'POST' and form.validate_on_submit():
        current_user.receive_daily_report = form.receive_daily_report.data

        if current_user.receive_daily_report and form.daily_report_time.data:
            try:
                current_user.daily_report_time = form.daily_report_time.data
                flash(f'Set to receive daily reports at {current_user.daily_report_time.strftime("%H:%M")}.')
            except ValueError:
                # In case the time_str doesn't match the expected format '%H:%M'
                flash('Invalid format for daily report time. Please use HH:MM format.', 'error')
                # Optionally, redirect back to the form to correct the error
                return redirect(url_for('report_bp.report_preferences'))
        else:
            current_user.daily_report_time = None
            flash('Opted out of daily reports.')

        current_user.receive_monthly_report = form.receive_monthly_report.data

        if current_user.receive_monthly_report:
            current_user.monthly_report_date = int(form.monthly_report_date.data)
            flash(f'Set to receive monthly reports on day {current_user.monthly_report_date} of each month.')
        else:
            current_user.monthly_report_date = None
            flash('Opted out of monthly reports.')

        db.session.commit()
        flash('Your report preferences have been updated.')
        return redirect(url_for('report_bp.report_preferences'))

    return render_template('report.html', form=form)
