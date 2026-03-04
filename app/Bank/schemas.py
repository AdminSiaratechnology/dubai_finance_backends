
from pydantic import BaseModel, Field
from typing import Optional,List
from app.loantype.schemas import LoanStatus, LoanTypeOut
from app.category.schemas import CategoryOut


class BankBase(BaseModel):
    name: str
    short_code: str
    default_tat_days: int = 0
    description: Optional[str] = None
    status: LoanStatus = LoanStatus.active
    # logo_url: Optional[str] = None
    
    


class BankCreate(BankBase):
    category_id: int | None = None
    loan_type_ids: list[int] | None = None


class BankUpdate(BaseModel):
    name: Optional[str] = None
    short_code: Optional[str] = None
    default_tat_days: Optional[int] = None
    description: Optional[str] = None
    status: Optional[LoanStatus] = None
    logo_url: Optional[str] = None
    category_id: Optional[int] = None
    loan_type_ids: Optional[List[int]] = None


class BankOut(BankBase):
    id: int
    # category_id: int | None = None   
    category: CategoryOut | None = None   # 👈 yaha change
    loan_types: list[LoanTypeOut] = []
    logo_url: str | None = None

    model_config = {
        "from_attributes": True
    }







class PaginatedBankOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[BankOut]

