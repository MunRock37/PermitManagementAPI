# app/tasks.py

from celery import Celery
from app import crud, models
from app.config import settings
from app.database import SessionLocal
import os

import app.beat_scheduler

celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0"),
)

@celery_app.task
def expire_pending_permits():
    print("Running expire_pending_permits...")
    db = SessionLocal()
    expired = crud.get_pending_expired_permits(db)
    for permit in expired:
        crud.update_permit_status(db, permit.id, models.PermitStatus.expired)
    db.close()
