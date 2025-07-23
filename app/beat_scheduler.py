from app.tasks import celery_app

celery_app.conf.beat_schedule = {
    "expire-every-30-seconds": {
        "task": "app.tasks.expire_pending_permits",
        "schedule": 30.0,  # every 30 seconds
    },
}
celery_app.conf.timezone = "UTC"
