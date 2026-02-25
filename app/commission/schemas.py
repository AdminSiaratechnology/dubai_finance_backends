
from pydantic import BaseModel, Field

################# Loan Type ###################

class LoanBase(BaseModel):
    name: str

class LoanCreate(LoanBase):
    pass

class LoanTypeOut(LoanBase):
    id: int
    name: str
    model_config = {
        "from_attributes": True
    }
