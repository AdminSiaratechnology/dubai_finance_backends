from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class LeadBase(BaseModel):
    customer_name: str
    mobile_number: str
    email: EmailStr
    product_id: int
    requested_amount: float


# Agent sirf ye fields bhejega
class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    customer_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    product_id: Optional[int] = None
    requested_amount: Optional[float] = None
    status: Optional[str] = None


class LeadOut(LeadBase):
    id: int
    agent_id: int
    telecaller_id: Optional[int] = None
    # status: str
    created_at: datetime

    class Config:
        from_attributes = True