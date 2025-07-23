from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app import models, schemas


def create_permit(db: Session, permit: schemas.PermitCreate):
    new_permit = models.Permit(**permit.dict())
    db.add(new_permit)
    db.commit()
    db.refresh(new_permit)
    return new_permit


def get_permits(db: Session, status: str = None):
    query = db.query(models.Permit)
    if status:
        query = query.filter(models.Permit.status == status)
    return query.all()


# def update_permit_status(db: Session, permit_id: int, status: models.PermitStatus):
#     permit = db.query(models.Permit).get(permit_id)
#     if permit:
#         permit.status = status
#         db.commit()
#         db.refresh(permit)
#     return permit


# def get_pending_expired_permits(db: Session):
#     threshold = datetime.utcnow() - timedelta(seconds=30)
#     return (
#         db.query(models.Permit)
#         .filter(
#             models.Permit.status == models.PermitStatus.pending,
#             models.Permit.created_at < threshold,
#         )
        # .all()
    # )


def get_pending_expired_permits(db: Session):
    # threshold = datetime.utcnow() - timedelta(seconds=30)
    threshold = datetime.utcnow() - timedelta(minutes=2)
    return db.query(models.Permit).filter(
        models.Permit.status == models.PermitStatus.pending,
        models.Permit.created_at < threshold
    ).all()

def update_permit_status(db: Session, permit_id: int, new_status: models.PermitStatus):
    permit = db.query(models.Permit).get(permit_id)
    if permit:
        permit.status = new_status
        db.commit()
        db.refresh(permit)