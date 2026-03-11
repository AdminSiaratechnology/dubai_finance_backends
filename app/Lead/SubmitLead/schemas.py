from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from app.loantype.schemas import BankLite


class LeadBase(BaseModel):
    customer_name: str
    mobile_number: str
    email: EmailStr
    
    
    requested_amount: float


# Agent sirf ye fields bhejega
class LeadCreate(LeadBase):
    product_id: Optional[int] = None
    bank_id: Optional[int] = None
    


class LeadUpdate(BaseModel):
    customer_name: Optional[str] = None
    mobile_number: Optional[str] = None
    email: Optional[EmailStr] = None
    product_id: Optional[int] = None
    bank_id: Optional[int] = None
    requested_amount: Optional[float] = None
    status: Optional[str] = None




# --------------------------- Product Lite ----------------------------

class CaseLite(BaseModel):
    id: int
    status: str
    requested_amount: float

    class Config:
        from_attributes = True

class ProductLite(BaseModel):
    id: int
    product_name: str

    model_config = {"from_attributes": True}

class LeadOut(LeadBase):
    id: int
    agent_id: int
    telecaller_id: Optional[int] = None
    product: ProductLite
    bank: Optional[BankLite]
    case: Optional[CaseLite] = None   # 👈 yaha add karo
    # status: str
    created_at: datetime

    class Config:
        from_attributes = True
        from_attributes = True