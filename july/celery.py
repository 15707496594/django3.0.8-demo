import os

from celery import Celery
from datetime import timedelta

QUEUES = {
    # ‘方法名’                  ‘队列名’
    'demo.tasks.hello_world': 'demo_hello_world'
}

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'july.settings')

app = Celery('july')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# app.autodiscover_tasks(packages=['demo',])
app.conf.task_routes = {
    'demo.tasks.hello_world': {'queue': QUEUES['demo.tasks.hello_world']}
}

app.conf.beat_schedule = {
    'add-every-10-second-demo_hello_world': {
        'task': 'demo.tasks.hello_world',
        'schedule': timedelta(seconds=10),
        'args': (),
    },
}
