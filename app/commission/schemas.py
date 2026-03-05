from pydantic import BaseModel
from datetime import date, datetime
from enum import Enum
from typing import Optional
from app.loantype.schemas import BankLite
from app.product.schemas import ProductLite

class CommissionType(str, Enum):
    percentage = "percentage"
    flat = "flat"

class CommissionStatus(str, Enum):
    active = "active"
    inactive = "inactive"    


class CommissionBase(BaseModel):
   

    commission_type: CommissionType
    commission_value: float

    agent_share: Optional[float] = 0
    telecaller_share: Optional[float] = 0
    coordinator_share: Optional[float] = 0

    effective_from_date: date

    status: CommissionStatus = CommissionStatus.active



class CommissionCreate(CommissionBase):
    bank_id: int
    product_id: int


class CommissionUpdate(BaseModel):
    commission_type: Optional[CommissionType]
    commission_value: Optional[float]

    agent_share: Optional[float]
    telecaller_share: Optional[float]
    coordinator_share: Optional[float]

    effective_from_date: Optional[date]
    status: Optional[CommissionStatus]


class CommissionOut(CommissionBase):
    id: int
    bank: BankLite
    product: ProductLite
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True    





class PaginatedCommissionOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[CommissionOut]
