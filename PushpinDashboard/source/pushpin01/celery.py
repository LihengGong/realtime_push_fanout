import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pushpin01.settings')

app = Celery('pushpin01', broker='amqp://')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
