import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reporting_app.settings')

app = Celery('reporting_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
