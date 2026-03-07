


from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum
from typing import Optional, List

from app.commission.schemas import CommissionOut




# ---------------- STATUS ENUM ----------------
class AgentStatus(str, Enum):
    active = "active"
    inactive = "inactive"





# ---------------- BASE SCHEMA ----------------
class AgentBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    emirates_id: str
    nationality: str
    bussiness_name: str
    year_of_experience: int
    

    account_holder_name: str
    bank_name: str
    account_number: str
    iban: str

    status: AgentStatus = AgentStatus.active

# ---------------- CREATE SCHEMA ----------------
class AgentCreate(AgentBase):
    password: str
    commission_ids: Optional[List[int]] = []
    
# ---------------- UPDATE SCHEMA ----------------
class AgentUpdate(BaseModel):

    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    emirates_id: Optional[str] = None
    nationality: Optional[str] = None
    year_of_experience: Optional[int] = None

    account_holder_name: Optional[str] = None
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    iban: Optional[str] = None

    status: Optional[str] = None


# ---------------- RESPONSE SCHEMA ----------------
class AgentOut(BaseModel):
    id: int
    user_id: int
    name: str
    email: EmailStr
    phone: str
    emirates_id: str
    nationality: str
    experience: int

    account_holder_name: str
    bank_name: str
    account_number: str
    iban: str
    status: AgentStatus
    # commission_ids: List[int] = []
    commissions: List[CommissionOut] = []
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True





class PaginatedAgentOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[AgentOut]
    