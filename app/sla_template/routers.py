from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.sla_template.schemas import TemplateOut, SlaTemplateCreate
from app.account.deps import require_admin
from app.db.config import SessionDep
from app.account.models import User

router = APIRouter()


# ✅ Create Category
@router.post("", response_model=TemplateOut)
async def category_create(
    session: SessionDep,
    slatemplate: SlaTemplateCreate,
    admin_user: User = Depends(require_admin)
):
    return await create_category(session, category)