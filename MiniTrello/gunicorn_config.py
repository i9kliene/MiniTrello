"""Gunicorn config file"""
import os

# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "MiniTrello.wsgi:application"
# The granularity of Error log outputs
loglevel = "debug"
# The number of worker processes for handling requests
workers = 2
threads = 2
# logs
accesslog = "-"
errorlog = "-"
# The socket to bind
bind = "0.0.0.0:8000"
# Restart workers when code changes (development only!)
if os.getenv("DEBUG"):
    reload = True
