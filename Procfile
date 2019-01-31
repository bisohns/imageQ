release: python manage.py migrate
web: gunicorn --env DJANGO_SETTINGS_MODULE=ImageQ.settings.production ImageQ.wsgi --log-file - --log-level debug
