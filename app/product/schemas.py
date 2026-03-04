from pydantic import BaseModel, Field
import enum
from app.commission.schemas import BankLite, LoanTypeLite
from app.sla_template.schemas import SLATemplateLite
from typing import Optional,List


################ Product ##################


class ProductStatus(enum.Enum):
    active = "active"
    inactive = "inactive"

class CustomerSegment(enum.Enum):
    salaried = "Salaried"
    selfemployed = "Self-employed"
    sme = "SME"

class ProductBase(BaseModel):
    # Basic Info
    product_name: str
    customer_segment: CustomerSegment

    # Foreign Keys
    

    # Loan Limits & Tenure
    min_loan_amount: float = Field(ge=0)
    max_loan_amount: float = Field(ge=0)

    min_tenure: int = Field(ge=0)
    max_tenure: int = Field(ge=0)

    # Configuration & Settings
    processing_fee: float = Field(default=0, ge=0)
    priority_score: int = Field(default=50, ge=0, le=100)

    internal_notes: Optional[str] = None
    status: ProductStatus = ProductStatus.active


class ProductCreate(ProductBase):
    bank_id: int
    loan_type_id: int
    sla_template_id: int


class ProductOut(ProductBase):
    id: int
    # 🔥 Nested objects instead of IDs
    bank: BankLite
    loan_type: LoanTypeLite
    sla_template: SLATemplateLite
   
    model_config = {
        "from_attributes": True
    }





class PaginatedProductOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[ProductOut]





