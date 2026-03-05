
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional, List


# ---------------- STATUS ENUM ----------------
class CoordinatorStatus(str, Enum):
    active = "active"
    inactive = "inactive"


# ---------------- BASE SCHEMA ----------------
class CoordinatorBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    emirates_id: str
    nationality: str
    experience: int

    account_holder_name: str
    bank_name: str
    account_number: str
    iban: str

    status: CoordinatorStatus = CoordinatorStatus.active


# ---------------- CREATE SCHEMA ----------------
class CoordinatorCreate(CoordinatorBase):
    password: str


# ---------------- UPDATE SCHEMA ----------------
class CoordinatorUpdate(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None
    emirates_id : Optional[str] = None
    nationality: Optional[str] = None
    experience: Optional[int] = None

    account_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    iban: Optional[str] = None

    status: str


# ---------------- RESPONSE SCHEMA ----------------
class CoordinatorOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    emirates_id: str
    nationality: str
    experience: int

    account_holder_name: str
    bank_name: str
    account_number: str
    iban: str

    status: CoordinatorStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------- PAGINATION RESPONSE ----------------
class PaginatedCoordinator(BaseModel):
    total: int
    page: int
    limit: int
    items: List[CoordinatorOut]
