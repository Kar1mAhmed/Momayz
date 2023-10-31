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
    'donkey_run': {
        'task': 'settings.tasks.test_func',
        'schedule': crontab(hour=13, minute=53),
        # 'args': (1, 1)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
