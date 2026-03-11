from sqlalchemy.ext.asyncio import AsyncSession
from app.Lead.SubmitLead.models import Lead, EmailOTP
from app.Lead.SubmitLead.schemas import LeadCreate
from sqlalchemy import select, delete, or_
from app.account.models import User, UserRole
from fastapi import HTTPException
import random
from datetime import datetime, timedelta
from app.account.utils import send_email
from typing import Optional


# async def get_all_leads(
#     db: AsyncSession,
#     skip: int = 0,
#     limit: int = 100,
#     search: Optional[str] = None
# ):
#     query = select(Lead).order_by(Lead.created_at.desc())

#     if search:
#         query = query.where(
#             or_(
#                 Lead.customer_name.ilike(f"%%{search}%%"),
#                 Lead.mobile_number.ilike(f"%%{search}%%"),
#                 Lead.email.ilike(f"%%{search}%%")
#             )
#         )

#     result = await db.execute(query.offset(skip).limit(limit))
#     leads = result.scalars().all()
#     return leads


async def get_all_leads(
    db: AsyncSession,
    user,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
):

    query = select(Lead).order_by(Lead.created_at.desc())

    # 🔹 Role based filter
    if user.role == "agent":
        query = query.where(Lead.agent_id == user.id)

    elif user.role == "telecaller":
        query = query.where(Lead.telecaller_id == user.id)

    elif user.role == "admin":
        pass  # admin ko sab data dikhega

    # 🔹 Search filter
    if search:
        query = query.where(
            or_(
                Lead.customer_name.ilike(f"%{search}%"),
                Lead.mobile_number.ilike(f"%{search}%"),
                Lead.email.ilike(f"%{search}%")
            )
        )

    result = await db.execute(query.offset(skip).limit(limit))
    leads = result.scalars().all()

    return leads



    
async def get_lead_by_id(db: AsyncSession, lead_id: int):
    result = await db.execute(select(Lead).where(Lead.id == lead_id))
    lead = result.scalars().first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead


async def send_lead_otp(db: AsyncSession, email: str):

    otp = str(random.randint(100000, 999999))

    # remove old otp
    await db.execute(
        delete(EmailOTP).where(EmailOTP.email == email)
    )

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_record)
    await db.commit()

    await send_email(
        session=db,
        to_email=email,
        subject="Lead Verification OTP",
        body=f"Your OTP is {otp}. It will expire in 5 minutes."
    )

    return {"message": "OTP sent successfully"}


async def verify_otp_and_submit_lead(
    db: AsyncSession,
    lead_data: LeadCreate,
    otp: str,
    user: User
):

    result = await db.execute(
        select(EmailOTP).where(EmailOTP.email == lead_data.email)
    )

    otp_record = result.scalars().first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="OTP not found")

    if otp_record.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    # delete otp after verification
    await db.delete(otp_record)

    # find telecaller
    # get all active telecallers
    result = await db.execute(
        select(User).where(
            User.role == UserRole.TELECALLER,
            User.is_active == True
        ).order_by(User.id)
    )

    telecallers = result.scalars().all()

    if not telecallers:
        telecaller = None
    else:
        # count total leads
        result = await db.execute(select(Lead))
        total_leads = len(result.scalars().all())

        # round robin index
        index = total_leads % len(telecallers)

        telecaller = telecallers[index]

    new_lead = Lead(
        agent_id=user.id,
        telecaller_id=telecaller.id if telecaller else None,
        customer_name=lead_data.customer_name,
        mobile_number=lead_data.mobile_number,
        email=lead_data.email,
        bank_id=lead_data.bank_id,
        product_id=lead_data.product_id,
        requested_amount=lead_data.requested_amount
    )

    db.add(new_lead)
    await db.commit()
    await db.refresh(new_lead)

    return new_lead
