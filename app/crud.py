from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app import models, schemas


def create_permit(db: Session, permit: schemas.PermitCreate):
    """
    Create a new permit in the database.

    Args:
        db (Session): Database session.
        permit (PermitCreate): Data for the new permit.

    Returns:
        Permit: The newly created permit.
    """
    new_permit = models.Permit(**permit.dict())
    db.add(new_permit)
    db.commit()
    db.refresh(new_permit)
    return new_permit


def get_permits(db: Session, status: str = None):
    """
    Retrieve all permits, optionally filtered by status.

    Args:
        db (Session): Database session.
        status (str, optional): Filter by permit status.

    Returns:
        List[Permit]: List of permits.
    """
    query = db.query(models.Permit)
    if status:
        query = query.filter(models.Permit.status == status)
    return query.all()


def get_pending_expired_permits(db: Session):
    """
    Fetch all pending permits older than 2 minutes.

    Args:
        db (Session): Database session.

    Returns:
        List[Permit]: List of expired pending permits.
    """
    threshold = datetime.utcnow() - timedelta(minutes=2)
    return db.query(models.Permit).filter(
        models.Permit.status == models.PermitStatus.pending,
        models.Permit.created_at < threshold
    ).all()


def update_permit_status(db: Session, permit_id: int, new_status: models.PermitStatus):
    """
    Update the status of a permit.

    Args:
        db (Session): Database session.
        permit_id (int): ID of the permit to update.
        new_status (PermitStatus): New status to apply.

    Returns:
        Permit | None: Updated permit, or None if not found.
    """
    permit = db.query(models.Permit).get(permit_id)
    if permit:
        permit.status = new_status
        db.commit()
        db.refresh(permit)
        return permit
    return None
