import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('config')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'sweep-expired-bookings-every-5-mins': {
        'task': 'apps.rentals.tasks.sweep_expired_bookings',
        'schedule': crontab(minute='*/5'),
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
