web: celery -A project worker --pool=solo -l INFO && celery -A project beat -l INFO && daphne project.asgi:application --bind 0.0.0.0:$PORT -v2
