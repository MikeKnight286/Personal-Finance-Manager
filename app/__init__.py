from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_mail import Mail
from celery import Celery
import os

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Database Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') # Set in .env
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI') # Set in .env
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask-Mail Configuration
    app.config['MAIL_SERVER'] = 'smtp.gmail.com' # Using gmail simple mail transfer protocol service
    app.config['MAIL_PORT'] = 587 
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME') # Set in .env
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # Set in .env (App password generated from gmail for your account)
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME') # Set in .env 

    # Celery Configuration
    app.config['broker_url'] = os.getenv('CELERY_BROKER_URL') # Set in .env 
    app.config['result_backend'] = os.getenv('CELERY_RESULT_BACKEND') # Set in .env 

    # Initializing database, login manager and mail
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # Define the user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.users_model import User  # Imporing here to avoid circular dependencies
        return User.query.get(int(user_id))

    # Import models
    from .models.transaction_model import Transaction
    from .models.savings_model import SavingGoal

    # Import and register your authentication Blueprint
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    # Register other Blueprints
    from .views.home_bp import home_bp
    from .views.dashboard_bp import dashboard_bp
    from .views.report_bp import report_bp
    from .views.transaction_record_bp import add_record_bp
    from .views.saving_goals_bp import saving_goals_bp
    app.register_blueprint(home_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(add_record_bp)
    app.register_blueprint(saving_goals_bp)

    return app


