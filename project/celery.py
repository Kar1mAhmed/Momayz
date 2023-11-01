from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Cairo')

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    'daily_midnight': {
        'task': 'settings.tasks.midnight_call',
        'schedule': crontab(hour=0, minute=0)
    },
    
    'flight_notification': {
        'task': 'settings.tasks.notify_before_30min',
        'schedule': crontab(hour=15, minute=15)
    },
}

app.autodiscover_tasks()
