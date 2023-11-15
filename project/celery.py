from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

from django_celery_beat.models import PeriodicTask

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.conf.enable_utc = False

app.conf.update(timezone = 'Africa/Cairo')

app.config_from_object(settings, namespace='CELERY')


app.conf.beat_schedule = {
    'flight_notification': {
        'task': 'settings.tasks.flight_notification',
        'schedule': crontab(minute='*/30', hour='6-18')
    },
    
    'midnight': {
        'task': 'settings.tasks.midnight',
        'schedule': crontab(minute=0, hour=0)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')