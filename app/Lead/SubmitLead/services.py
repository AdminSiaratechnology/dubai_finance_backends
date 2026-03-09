


from sqlalchemy.ext.asyncio import AsyncSession
from app.Lead.SubmitLead.models import Lead
from app.Lead.SubmitLead.schemas import LeadCreate
from sqlalchemy import select
from app.account.models import User, UserRole


async def submit_lead(
    db: AsyncSession,
    lead_data: LeadCreate,
    user: User
) -> Lead:

    # find available telecaller (simple example)
    result = await db.execute(
        select(User).where(
            User.role == UserRole.TELECALLER,
            User.is_active == True
        )
    )

    telecaller = result.scalars().first()

    new_lead = Lead(
        agent_id=user.id,
        telecaller_id=telecaller.id if telecaller else None,
        customer_name=lead_data.customer_name,
        mobile_number=lead_data.mobile_number,
        email=lead_data.email,
        product_id=lead_data.product_id,
        requested_amount=lead_data.requested_amount
    )

    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)

    return new_lead