
from sqlalchemy.ext.asyncio import AsyncSession
from app.sla_template.schemas import SlaTemplateCreate, TemplateOut
from sqlalchemy import select
from fastapi import HTTPException, status
from app.sla_template.models import SLATemplate

# ✅ Create Category
async def create_category(
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
        auto_revert_enabled=slatemplate.escalation_after,
        # status=category.status
    )

    # session.add(new_category)
    # await session.commit()
    # await session.refresh(new_category)

    # return new_category
