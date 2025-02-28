#!/bin/bash
#set -e


# Avvia il server Django
echo "Avviando il server Django..."
if [[ "$DEBUG" == "True" ]]; then
  echo "Starting debug server"
  #python manage.py runserver 0.0.0.0:8000
  python -m gunicorn sadicweb.config.wsgi -b 0.0.0.0:8000 --capture-output
else
  echo "Starting prod gunicorn server"
  python -m gunicorn sadicweb.config.wsgi -b 0.0.0.0:8000 --capture-output --workers=3 --threads=2 --timeout 600
fi
