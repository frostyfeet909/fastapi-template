from celery import Celery
from config.redis_config import settings

app = Celery("tasks", broker=settings.CELERY_BROKER_URI, backend=settings.CELERY_BROKER_URI)
