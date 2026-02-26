
from pydantic import BaseModel, Field
import enum

from typing import Optional,List

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



########################################## Category#########################################    




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




# --------------------------------------------------------------- Bank Schemas -----------------------------



class BankBase(BaseModel):
    name: str
    short_code: str
    default_tat_days: int = 0
    description: Optional[str] = None
    status: LoanStatus = LoanStatus.active
    logo_url: Optional[str] = None
    category_id: Optional[int] = None
    loan_type_ids: Optional[List[int]] = None


class BankCreate(BankBase):
    pass


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

    model_config = {
        "from_attributes": True
    }
