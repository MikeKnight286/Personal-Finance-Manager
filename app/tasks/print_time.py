from datetime import datetime
from celery import Celery
from flask_mail import Message
from app import create_app, db, mail
from app.models.users_model import User  
from app.models.transaction_model import Transaction
from app.views.report_bp import generate_report_html, send_email 

def register_tasks(celery):
    @celery.task(name='app.tasks.print_time')
    def print_time():
        print(f"Current Time: {datetime.now()}")