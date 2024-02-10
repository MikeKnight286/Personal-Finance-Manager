from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    transactions = db.relationship('Transaction', backref='user', lazy=True)
    saving_goals = db.relationship('SavingGoal', backref='user', lazy=True)
    receive_daily_report = db.Column(db.Boolean, default=False)
    daily_report_time = db.Column(db.Time)  # Time of day the user prefers to receive the daily report
    receive_monthly_report = db.Column(db.Boolean, default=False)
    monthly_report_date = db.Column(db.Integer)  # Day of the month the user prefers to receive the monthly report
