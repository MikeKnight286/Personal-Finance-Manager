from celery import Celery
from flask import Flask

def make_celery(app: Flask) -> Celery:
    celery = Celery(app.import_name, broker=app.config['broker_url'])
    celery.conf.update(app.config)

    from app.celery_config import CELERY_BEAT_SCHEDULE
    celery.conf.beat_schedule = CELERY_BEAT_SCHEDULE

    class ContextTask(celery.Task):
        """
        Makes the Flask app context available to Celery tasks.
        """
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    return celery

# Import the Flask app instance
from app import create_app

app = create_app()
celery = make_celery(app)

# Registering tasks
from app.tasks import scheduled_reports
scheduled_reports.register_report_tasks(celery)
