from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import crud, database, models, schemas
from app.auth import get_current_user

database.init_db()
app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/permits", response_model=schemas.PermitResponse)
def create_permit(
    permit: schemas.PermitCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return crud.create_permit(db, permit)


@app.get("/permits", response_model=List[schemas.PermitResponse])
def list_permits(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    return crud.get_permits(db, status)


@app.post("/permits/{permit_id}/approve", response_model=schemas.PermitResponse)
def approve_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    permit = crud.update_permit_status(db, permit_id, models.PermitStatus.approved)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit


@app.post("/permits/{permit_id}/revoke", response_model=schemas.PermitResponse)
def revoke_permit(
    permit_id: int,
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user),
):
    permit = crud.update_permit_status(db, permit_id, models.PermitStatus.revoked)
    if not permit:
        raise HTTPException(status_code=404, detail="Permit not found")
    return permit
