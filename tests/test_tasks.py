from datetime import timedelta

from app import crud, schemas, tasks
from app.database import SessionLocal


def test_expire_old_permits():
    db = SessionLocal()
    permit = crud.create_permit(
        db, schemas.PermitCreate(name="Bob", license_plate="XYZ456", address="Elm St")
    )
    # simulate >5 mins old
    permit.created_at = permit.created_at.replace(minute=permit.created_at.minute - 6)
    permit.created_at = permit.created_at - timedelta(minutes=6)
    db.commit()

    tasks.expire_pending_permits()
    db.refresh(permit)
    assert permit.status == "expired"
    db.close()
