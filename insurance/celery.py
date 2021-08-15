import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insurance.settings')

app = Celery('insure_your_buddy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
