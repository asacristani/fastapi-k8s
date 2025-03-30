import os

from celery import Celery

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
)


@celery_app.task
def ping_task():
    return "pong"


@celery_app.task
def scheduled_hello():
    print("[Scheduled] Hello from Celery!")
