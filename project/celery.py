import os 
from celery import Celery 
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program. 
os.environ.setdefault ('DJANGO_SETTINGS_MODULE', 'project.settings') 

app = Celery('project') 

# Using a string here means the worker doesn't 
# have to serialize the configuration object to 
# child processes. - namespace='CELERY' means all 
# celery-related configuration keys should 
# have a `CELERY_` prefix. 
app.config_from_object('django.conf:settings', namespace='CELERY') 

app.conf.beat_schedule = {
    'run_at_midnight': {
        'task': 'settings.tasks.midnight_call',
        'schedule': crontab(hour=13, minute=26),
        'args': (1, 1)
    },
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
