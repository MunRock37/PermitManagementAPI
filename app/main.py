from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, database, models, schemas
from app.auth import get_current_user

database.init_db()

app = FastAPI(
    title="Permit Management API",
    description="""
    RESTful API to manage residential parking permits.

    Features:
    - Apply for a permit
    - Approve or revoke permits
    - Filter permits by status
    - Background job auto-expires pending permits after 2 minutes
    """,
    version="1.0.0"
)


def get_db():
    """Dependency to get DB session."""
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/permits", response_model=schemas.PermitResponse, summary="Create a new permit")
def create_permit(
    permit: schemas.PermitCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Create a new parking permit with status set to `pending`.

    - **name**: Name of the applicant
    - **license_plate**: Vehicle license plate
    - **address**: Address of the applicant

    Returns the created permit.
    """
    return crud.create_permit(db, permit)


@app.get("/permits", response_model=List[schemas.PermitResponse], summary="List permits")
def list_permits(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    List all parking permits.

    - Optional query param: `status` = pending | approved | revoked | expired
    - Returns a list of permits (filtered by status if provided).
    """
    return crud.get_permits(db, status)


@app.post("/permits/{permit_id}/approve", response_model=schemas.PermitResponse, summary="Approve a permit")
def approve_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Approve a permit by ID.

    Changes permit status to `approved`.
    Returns the updated permit.
    """
    permit = crud.update_permit_status(db, permit_id, models.PermitStatus.approved)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit


@app.post("/permits/{permit_id}/revoke", response_model=schemas.PermitResponse, summary="Revoke a permit")
def revoke_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    """
    Revoke a permit by ID.

    Changes permit status to `revoked`.
    Returns the updated permit.
    """
    permit = crud.update_permit_status(db, permit_id, models.PermitStatus.revoked)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit
