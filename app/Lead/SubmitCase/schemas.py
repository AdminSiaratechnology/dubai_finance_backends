from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
class CaseBase(BaseModel):
    customer_name: str
    mobile_number: str
    email: EmailStr
    product_type: int
    requested_amount: float


class CaseCreate(CaseBase):
    agent_id: int
    lead_id: Optional[int] = None
    salary: Optional[float] = None
    company_name: Optional[str] = None
    emirates_id: Optional[str] = None
    passport_no: Optional[str] = None


class CaseUpdate(BaseModel):
    salary: Optional[float] = None
    company_name: Optional[str] = None
    emirates_id: Optional[str] = None
    passport_no: Optional[str] = None
    status: Optional[str] = None


class CaseOut(CaseBase):
    id: int
    agent_id: int
    lead_id: Optional[int]
    salary: Optional[float]
    company_name: Optional[str]
    emirates_id: Optional[str]
    passport_no: Optional[str]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True



class PaginatedCase(BaseModel):
    total: int
    page: int
    limit: int
    data: List[CaseOut]