release: python manage.py migrate
web: gunicorn ImageQ.wsgi --log-file - --log-level debug
