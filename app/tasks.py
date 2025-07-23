import os

from celery import Celery

from app import crud, models
from app.config import settings
from app.database import SessionLocal

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)


@celery_app.task
def expire_pending_permits():
    print("Task triggered: expire_pending_permits")
    db = SessionLocal()
    expired = crud.get_pending_expired_permits(db)
    for permit in expired:
        print(f" Expiring permit: {permit.id}")
        crud.update_permit_status(db, permit.id, models.PermitStatus.expired)
    db.close()


celery_app.conf.beat_schedule = {
    "expire-pending-permits-every-minute": {
        "task": "app.tasks.expire_pending_permits",
        "schedule": 60.0,  # every 60 seconds
    }
}
celery_app.conf.timezone = "UTC"
