from datetime import datetime
from enum import Enum

from pydantic import BaseModel, StrictStr


class PermitCreate(BaseModel):
    name: StrictStr
    license_plate: StrictStr
    address: StrictStr


class PermitStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    revoked = "revoked"
    expired = "expired"


class PermitResponse(PermitCreate):
    id: int
    status: PermitStatus
    created_at: datetime

    class Config:
        orm_mode = True
