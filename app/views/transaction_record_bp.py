from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from app.models.transaction_model import Transaction  # Adjust the import path as needed
from datetime import datetime

add_record_bp = Blueprint('add_record_bp', __name__, url_prefix='/add_record')

@add_record_bp.route('/', methods=['GET', 'POST'])
@login_required
def add_record():
    if request.method == 'POST':
        # Retrieve form data
        transaction_type = request.form.get('type')
        category = request.form.get('category')
        amount = request.form.get('amount')
        date_str = request.form.get('date')
        time_str = request.form.get('time')  # Time input is optional
        description = request.form.get('description')

        # Validate required fields
        if not transaction_type or not category or not amount or not date_str:
            flash('Please fill in all required fields.')
            return render_template('transaction_record.html')

        # Defining a datetime object from date and time
        try:
            amount = float(amount)
            if time_str:  # If time is provided, combine it with the date
                date_time_str = f"{date_str} {time_str}"
                date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M')
            else:  # If no time is provided, use default time (00:00)
                date_time = datetime.strptime(date_str, '%Y-%m-%d')
        except ValueError as e:
            flash(f'Invalid input for amount, date, or time: {e}')
            return render_template('transaction_record.html')

        # Create a new Transaction record
        new_transaction = Transaction(
            user_id=current_user.id,
            type=transaction_type,
            category=category,
            amount=amount,
            date=date_time,  # Save the combined date and time
            description=description
        )

        # Add to database and commit
        db.session.add(new_transaction)
        db.session.commit()

        flash('Transaction added successfully.')
        return redirect(url_for('add_record_bp.add_record'))

    # If GET request or any other method, just display the form
    return render_template('transaction_record.html')
