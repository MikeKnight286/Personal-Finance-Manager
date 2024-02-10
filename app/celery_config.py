# celery_config.py
from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()

def make_celery(app_name, broker, backend):
    celery = Celery(app_name, broker=broker, backend=backend)
    return celery