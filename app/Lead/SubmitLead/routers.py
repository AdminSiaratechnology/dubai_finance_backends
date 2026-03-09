from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.account.deps import get_current_user
from app.Lead.SubmitLead.schemas import LeadOut, LeadCreate
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.Lead.SubmitLead.services import send_lead_otp, verify_otp_and_submit_lead



router = APIRouter()

@router.post("/send-otp")
async def send_otp(
    email: str,
    session: SessionDep,
    user: User = Depends(get_current_user)
):
    return await send_lead_otp(session, email)

@router.post("", response_model=LeadOut)
async def submit_lead_create(
    session: SessionDep,
    lead_data: LeadCreate,
    otp: str,
    user: User = Depends(get_current_user)
):
    return await verify_otp_and_submit_lead(
        session,
        lead_data,
        otp,
        user
    )