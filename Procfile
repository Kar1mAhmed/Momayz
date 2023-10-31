web: celery -A project.celery worker --pool=solo -l INFO && celery -A project.celery beat -l INFO && daphne project.asgi:application --bind 0.0.0.0:$PORT -v2
