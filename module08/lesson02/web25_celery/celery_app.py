
from celery import Celery

app = Celery(
    'celery_demo',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=['tasks']
)

# Optional: Configure Celery Beat schedule for periodic tasks
app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'tasks.add',
        'schedule': 30.0,
        'args': (16, 16)
    },
    'multiply-every-1-minute': {
        'task': 'tasks.multiply',
        'schedule': 60.0,
        'args': (4, 5)
    },
}
app.conf.timezone = 'UTC'
