from celery import Celery
from celery.schedules import crontab

from app.core.config import get_settings

settings = get_settings()

celery_app = Celery(
    "deribit_tracker",
    broker=settings.celery_broker_url,
    include=["app.tasks.fetch_prices"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    beat_schedule={
        "fetch-deribit-prices-every-minute": {
            "task": "fetch_prices_task",
            "schedule": crontab(minute="*"),
        }
    },
)

