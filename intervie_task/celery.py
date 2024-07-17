from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установите переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'intervie_task.settings')

app = Celery('intervie_task')

# Используйте настройки Django по умолчанию
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически обнаруживайте задачи в установленных приложениях Django
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
