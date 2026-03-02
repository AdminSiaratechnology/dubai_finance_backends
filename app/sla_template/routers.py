from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.sla_template.schemas import TemplateOut, SlaTemplateCreate, PaginatedSlaTemplateOut, SLAStatus
from app.account.deps import require_admin
from app.db.config import SessionDep
from app.account.models import User
from app.sla_template.services import create_sla_template, get_all_sla_template,get_sla_template_by_id,update_sla_template, delete_sla_template


router = APIRouter()


# ✅ Create SLA Template
@router.post("", response_model=TemplateOut)
async def sla_template_create(
    session: SessionDep,
    slatemplate: SlaTemplateCreate,
    admin_user: User = Depends(require_admin)
):
    return await create_sla_template(session, slatemplate)




# ✅ Get All SLA Template (Pagination + Search + Status)
@router.get("", response_model=PaginatedSlaTemplateOut)
async def sla_template_list(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
    # status: Optional[SLAStatus] = SLAStatus.ACTIVE,
    status: Optional[SLAStatus] = Query(
        None,   # 👈 changed from LoanStatus.active
        description="Filter by loan status"
    ),
    admin_user: User = Depends(require_admin)
):
    return await get_all_sla_template(
        session,
        page,
        limit,
        search,
        status
    )


#  Get SLA Templae By ID 
@router.get("/{sla_template_id}", response_model=TemplateOut)
async def sla_template_detail(
    sla_template_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_sla_template_by_id(session, sla_template_id)


# update SLA Template 

@router.put("/{sla_template_id}", response_model=TemplateOut)
async def sla_template_update(
    sla_template_id: int,
    data: SlaTemplateCreate,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await update_sla_template(session, sla_template_id, data)
    

#  SLA DELETE 
@router.delete("/{sla_template_id}")
async def sla_template_delete(
    sla_template_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    result = await delete_sla_template(session, sla_template_id)
    
    return result