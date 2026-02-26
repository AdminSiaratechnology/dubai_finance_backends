
from pydantic import BaseModel, Field
import enum

from typing import Optional

################# Loan Type ###################

class LoanStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class LoanBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: LoanStatus = LoanStatus.active   # default active 

class LoanCreate(LoanBase):
    pass

class LoanTypeOut(LoanBase):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }






class PaginatedProductOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[LoanTypeOut]