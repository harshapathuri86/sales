import multiprocessing

bind = '0.0.0.0:8000'  # The address and port to bind to
workers = multiprocessing.cpu_count() * 2 + 1  # Number of worker processes
worker_class = 'gevent'  # The type of worker processes to use
timeout = 30  # The maximum time (in seconds) for a request to be processed

# Logging configuration
accesslog = '/var/log/gunicorn/access.log'  # File path for access logs
errorlog = '/var/log/gunicorn/error.log'  # File path for error logs
loglevel = 'info'  # Log level (debug, info, warning, error, critical)

# Django settings module
raw_env = ['DJANGO_SETTINGS_MODULE=backend.settings']
