"""
WSGI entry point for production servers (Gunicorn, PythonAnywhere, Waitress).
Usage:
  gunicorn -w 2 -b 0.0.0.0:$PORT wsgi:app
"""
from database import init_db
from app import app

# Ensure schema exists on cold start (safe / idempotent)
try:
    init_db()
except Exception as e:
    print(f'[wsgi] init_db warning: {e}')

# Gunicorn / uWSGI look for "application" or we export app
application = app
