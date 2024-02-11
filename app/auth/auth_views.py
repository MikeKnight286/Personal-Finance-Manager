from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from . import auth_bp  # Using the Blueprint from auth package
from app import db
from app.models.users_model import User  

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.dashboard'))  

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard_bp.dashboard'))  # Redirecting to dashboard after login
        else:
            flash('Invalid email or password')
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.home')) # Redirecting to home after logout

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_bp.dashboard')) # Redirecting to dashboard if user is registered

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user exists already
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already registered.')
            return redirect(url_for('auth.register'))

        # Create a new user with the form data. Hash the password so the plaintext version isn't saved for user privacy
        new_user = User(email=email, password=generate_password_hash(password, method='sha256'))

        # Add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to the login page
        return redirect(url_for('auth.login'))

    # If a GET (or any other method) we'll render the register template
    return render_template('auth/register.html')