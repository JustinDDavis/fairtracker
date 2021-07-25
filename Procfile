release: python src/manage.py migrate --noinput
web: gunicorn --pythonpath src config.wsgi --timeout 180
