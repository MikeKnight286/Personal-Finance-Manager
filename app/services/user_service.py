from flask_wtf import FlaskForm
from wtforms import BooleanField, TimeField, SelectField, SubmitField
from wtforms.validators import Optional

class ReportPreferencesForm(FlaskForm):
    receive_daily_report = BooleanField('Receive Daily Report')
    daily_report_time = TimeField('Preferred Time for Daily Report', format='%H:%M', validators=[Optional()])
    receive_monthly_report = BooleanField('Receive Monthly Report')
    monthly_report_date = SelectField('Preferred Date for Monthly Report', choices=[(str(day), str(day)) for day in range(1, 26)], validators=[Optional()])  # Up to 25
    submit = SubmitField('Save Preferences')

