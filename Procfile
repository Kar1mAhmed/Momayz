web: celery -A project worker --loglevel=info & python manage.py migrate && gunicorn project.wsgi  --bind 0.0.0.0:$PORT
