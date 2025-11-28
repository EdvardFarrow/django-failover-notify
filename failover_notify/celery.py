import os
from celery import Celery

# Указываем настройки Django по умолчанию
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relay_service.settings')

app = Celery('relay_service')

# Берем конфиг из settings.py, ключи с префиксом CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим tasks.py в приложениях
app.autodiscover_tasks()