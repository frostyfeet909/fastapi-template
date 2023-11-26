from config.redis_config import settings

app = None
client = None

if settings.NEED_CELERY_BROKER_URI:
    broker_uri = settings.CELERY_BROKER_URI.unicode_string()
    backend_uri = settings.CELERY_BACKEND_URI.unicode_string() if settings.CELERY_BACKEND_URI else None
    try:
        from celery import Celery

        app = Celery(
            "tasks",
            broker=broker_uri,
            backend=backend_uri,
        )
        print("[+] Created redis app on {0}/{1}".format(broker_uri, backend_uri))
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Celery is not installed.")

if settings.NEED_INSECURE_URI:
    try:
        import redis

        client = redis.from_url(settings.INSECURE_URI.unicode_string())
        print("[+] Created redis client on {0}".format(settings.INSECURE_URI))
    except ModuleNotFoundError:
        raise ModuleNotFoundError("Redis is not installed.")
