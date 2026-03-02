
from sqlalchemy.ext.asyncio import AsyncSession
from app.sla_template.schemas import SlaTemplateCreate, TemplateOut,SLAStatus
from sqlalchemy import select
from fastapi import HTTPException, status
from app.sla_template.models import SLATemplate
from typing import Optional
from app.sla_template.models import SLATemplate
from sqlalchemy import func


# ✅ Create Sla Template
async def create_sla_template(
    session: AsyncSession,
    slatemplate: SlaTemplateCreate
) -> TemplateOut:

    # 🔎 Check duplicate
    result = await session.execute(
        select(SLATemplate).where(SLATemplate.template_name == slatemplate.template_name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="template name already exists"
        )

    new_slatemplate = SLATemplate(
        template_name=slatemplate.template_name,
        telecaller_action_time=slatemplate.telecaller_action_time,
        coordinator_verification_time=slatemplate.coordinator_verification_time,
        submission_time_limit=slatemplate.submission_time_limit,
        escalation_after=slatemplate.escalation_after,
        auto_revert_enabled=slatemplate.auto_revert_enabled,
        status=slatemplate.status
    )

    session.add(new_slatemplate)
    await session.commit()
    await session.refresh(new_slatemplate)

    return new_slatemplate




# ✅ Get All SLA Template (Pagination + Search + Status)
async def get_all_sla_template(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[SLAStatus] = None
    
):

    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []

    # 🔎 Search
    if search:
        filters.append(
            SLATemplate.template_name.ilike(f"%{search.strip()}%")
        )

    # 🔹 Status filter
    if status:
        filters.append(SLATemplate.status == status)

    # ✅ Count
    count_stmt = select(func.count(SLATemplate.id)).where(*filters)
    total = (await session.execute(count_stmt)).scalar_one()

    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": [],
        }

    # ✅ Data Query
    stmt = (
        select(SLATemplate)
        .where(*filters)
        .order_by(SLATemplate.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)
    items = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items,
    }



# ✅ Get SLA Template By ID
async def get_sla_template_by_id(
    session: AsyncSession,
    sla_template_id: int
) -> TemplateOut:

    result = await session.execute(
        select(SLATemplate).where(SLATemplate.id == sla_template_id)
    )
    slatemplate = result.scalar_one_or_none()

    if not slatemplate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA Template not found"
        )

    return slatemplate


# ✅ Update SLA Template
async def update_sla_template(
    session: AsyncSession,
    sla_template_id: int,
    data: SlaTemplateCreate
) -> TemplateOut:

    result = await session.execute(
        select(SLATemplate).where(SLATemplate.id == sla_template_id)
    )
    slatemplate = result.scalar_one_or_none()

    if not slatemplate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA Template not found"
        )

    # 🔎 Check duplicate
    result = await session.execute(
        select(SLATemplate).where(
            SLATemplate.template_name == data.template_name,
            SLATemplate.id != sla_template_id
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="template name already exists"
        )

    slatemplate.template_name = data.template_name
    slatemplate.telecaller_action_time = data.telecaller_action_time
    slatemplate.coordinator_verification_time = data.coordinator_verification_time
    slatemplate.submission_time_limit = data.submission_time_limit
    slatemplate.escalation_after = data.escalation_after
    slatemplate.auto_revert_enabled = data.auto_revert_enabled
    slatemplate.status = data.status

    session.add(slatemplate)
    await session.commit()
    await session.refresh(slatemplate)

    return slatemplate





# ✅ Delete SLA Template
async def delete_sla_template(
    session: AsyncSession,
    sla_template_id: int
):

    result = await session.execute(
        select(SLATemplate).where(SLATemplate.id == sla_template_id)
    )
    slatemplate = result.scalar_one_or_none()

    if not slatemplate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="SLA Template not found"
        )

    await session.delete(slatemplate)
    await session.commit()
    return {"message": "SLA Template deleted successfully"}