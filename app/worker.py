from celery.schedules import crontab

from app.tasks import celery_app

celery_app.conf.beat_schedule = {
    "scheduled-hello-task": {
        "task": "app.tasks.scheduled_hello",
        "schedule": crontab(minute="*/1"),  # Every 1 minute
    },
}

celery_app.conf.timezone = "UTC"
