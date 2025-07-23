from datetime import datetime, timedelta

from app.database import SessionLocal
from app.models import Permit


def expire_old_permits():
    db = SessionLocal()
    permits = (
        db.query(Permit)
        .filter(
            Permit.status == "pending",
            Permit.created_at < datetime.utcnow() - timedelta(minutes=5),
        )
        .all()
    )
    for permit in permits:
        permit.status = "expired"
    db.commit()
    db.close()
