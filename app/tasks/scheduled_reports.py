from datetime import datetime
import pytz
from app.util import get_app_context
from app.models.users_model import User  
from app.models.transaction_model import Transaction
from app.views.report_bp import generate_report_html, send_email 

def register_report_tasks(celery):
    @celery.task(name='app.tasks.send_scheduled_reports', bind=True)
    def send_scheduled_reports(self):
        with get_app_context():
            timezone = pytz.timezone('Asia/Tokyo') # Change to desired timezone
            now = datetime.now(timezone)
            current_hour = now.hour
            current_minute = now.minute
            current_day = now.day
            users = User.query.all()
            for user in users:
                if user.receive_daily_report and user.daily_report_time:
                    if user.daily_report_time.hour == current_hour and user.daily_report_time.minute == current_minute:
                        send_daily_report_for_user(user)
                if user.receive_monthly_report and current_day == user.monthly_report_date:
                    send_monthly_report_for_user(user)

    def send_daily_report_for_user(user):
        timezone = pytz.timezone('Asia/Tokyo')
        today = datetime.now(timezone).date()
        transactions = Transaction.query.filter(
            Transaction.user_id == user.id,
            Transaction.date == today
        ).all()
        if transactions:
            report_html = generate_report_html(transactions, "Daily Report")
            send_email("Your Daily Report", user.email, report_html)

    def send_monthly_report_for_user(user):
        timezone = pytz.timezone('Asia/Tokyo')
        today = datetime.now(timezone)
        start_of_month = datetime(today.year, today.month, 1, tzinfo=timezone)
        transactions = Transaction.query.filter(
            Transaction.user_id == user.id,
            Transaction.date >= start_of_month,
            Transaction.date <= today
        ).all()
        if transactions:
            report_html = generate_report_html(transactions, "Monthly Report")
            send_email("Your Monthly Report", user.email, report_html)
