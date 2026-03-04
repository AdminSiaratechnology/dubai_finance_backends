
from pydantic import BaseModel, Field
from typing import Optional,List
from app.loantype.schemas import LoanStatus

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: LoanStatus = LoanStatus.active   # default active 



class CategoryCreate(CategoryBase):
    pass

class CategoryOut(CategoryBase):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }



class PaginatedCategoryOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[CategoryOut]





