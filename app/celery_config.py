from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'send-scheduled-reports-every-minute': {
        'task': 'app.tasks.send_scheduled_reports',  
        'schedule': crontab(minute='*'),  # Run the task at every minute
    },
}