from decouple import config # pyright: ignore[reportMissingImports] 
from celery import Celery

DJANGO_SETTINGS_MODULE = config('DJANGO_SETTINGS_MODULE', 'failover_notify.settings')

app = Celery('failover_notify')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()