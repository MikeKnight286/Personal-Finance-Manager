import celery
from celery.schedules import crontab
import pytz

celery.conf.update(
    timezone='Asia/Tokyo',
)

celery.conf.beat_schedule = {
    'send-scheduled-reports-every-day': {
        'task': 'app.services.scheduled_reports_bp.send_scheduled_reports',
        'schedule': crontab(minute='*'),  # Adjust the timing as per your needs
    }
}
