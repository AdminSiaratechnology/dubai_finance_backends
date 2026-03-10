from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class CaseDocumentOut(BaseModel):
    emirates_id_front_url: Optional[str]
    emirates_id_back_url: Optional[str]

    class Config:
        from_attributes = True


class CaseOut(BaseModel):
    id: int
    agent_id: int
    customer_name: str
    mobile_number: str
    email: Optional[str]

    product_type: Optional[int]
    requested_amount: float

    salary: Optional[float]
    company_name: Optional[str]

    emirates_id: Optional[str]
    passport_no: Optional[str]

    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CaseDetailOut(CaseOut):
    documents: Optional[List[CaseDocumentOut]]


class PaginatedCaseOut(BaseModel):
    total: int
    page: int
    limit: int
    items: List[CaseDetailOut]