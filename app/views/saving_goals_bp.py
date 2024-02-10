from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.savings_model import SavingGoal  # Adjust import path as needed
from datetime import datetime

saving_goals_bp = Blueprint('saving_goals_bp', __name__, url_prefix='/saving_goals')

@saving_goals_bp.route('/')
@login_required
def index():
    saving_goals = SavingGoal.query.filter_by(user_id=current_user.id).all()
    return render_template('saving_goals/saving_index.html', saving_goals=saving_goals)

@saving_goals_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        goal_name = request.form.get('goal_name')
        target_amount = float(request.form.get('target_amount'))
        current_amount = float(request.form.get('current_amount', 0.0))
        target_date = datetime.strptime(request.form.get('target_date'), '%Y-%m-%d')
        description = request.form.get('description', '')

        new_goal = SavingGoal(
            user_id=current_user.id,
            goal_name=goal_name,
            target_amount=target_amount,
            current_amount=current_amount,
            target_date=target_date,
            description=description
        )

        db.session.add(new_goal)
        db.session.commit()

        flash('Saving goal created successfully.')
        return redirect(url_for('saving_goals_bp.index'))

    return render_template('saving_goals/saving_create.html')

@saving_goals_bp.route('/<int:goal_id>/update', methods=['GET', 'POST'])
@login_required
def update(goal_id):
    saving_goal = SavingGoal.query.get_or_404(goal_id)

    if request.method == 'POST':
        saving_goal.goal_name = request.form.get('goal_name')
        saving_goal.target_amount = float(request.form.get('target_amount'))
        saving_goal.current_amount = float(request.form.get('current_amount', saving_goal.current_amount))
        saving_goal.target_date = datetime.strptime(request.form.get('target_date'), '%Y-%m-%d')
        saving_goal.description = request.form.get('description', saving_goal.description)

        db.session.commit()
        flash('Saving goal updated successfully.')
        return redirect(url_for('saving_goals_bp.index'))  # Redirecting to the index route

    saving_goal.target_date_formatted = saving_goal.target_date.strftime('%Y-%m-%d')
    # Before rendering the saving_update.html template
    if saving_goal.target_date:
        # Format the date as a string in the 'YYYY-MM-DD' format
        formatted_date = saving_goal.target_date.strftime('%Y-%m-%d')
    else:
        formatted_date = ''
    return render_template('saving_goals/saving_update.html', saving_goal=saving_goal)

@saving_goals_bp.route('/<int:goal_id>/delete', methods=['POST'])
@login_required
def delete(goal_id):
    saving_goal = SavingGoal.query.get_or_404(goal_id)
    db.session.delete(saving_goal)
    db.session.commit()
    flash('Saving goal deleted successfully.')
    return redirect(url_for('saving_goals_bp.index'))
