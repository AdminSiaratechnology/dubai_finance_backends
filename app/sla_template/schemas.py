from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal
import enum

class SLAStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class SLATemplateBase(BaseModel):
    template_name: str = Field(..., max_length=255)

    telecaller_action_time: int = Field(0, ge=0)
    coordinator_verification_time: int = Field(0, ge=0)
    submission_time_limit: int = Field(0, ge=0)
    escalation_after: int = Field(0, ge=0)

    auto_revert_enabled: bool = True
    status: SLAStatus = SLAStatus.ACTIVE




class SlaTemplateCreate(SLATemplateBase):
    pass

class TemplateOut(SLATemplateBase):
    id: int
    template_name: str
    model_config = {
        "from_attributes": True
    }





class PaginatedSlaTemplateOut(BaseModel):
    total: int
    page: int
    limit: int
    items: list[TemplateOut]

