from datetime import datetime
from pydantic import BaseModel

class CaseDocumentBase(BaseModel):
    document_type: str


class CaseDocumentCreate(CaseDocumentBase):
    case_id: int


class CaseDocumentOut(CaseDocumentBase):
    id: int
    case_id: int
    file_path: str
    uploaded_at: datetime

    class Config:
        from_attributes = True