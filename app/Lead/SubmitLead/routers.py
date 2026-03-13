from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from app.account.deps import get_current_user
from app.Lead.SubmitLead.schemas import LeadOut, LeadCreate
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.Lead.SubmitLead.services import (
    send_lead_otp, verify_otp_and_submit_lead, get_all_leads, get_lead_by_id
)



router = APIRouter()


@router.get("", response_model=List[LeadOut])
async def get_leads(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    lead_type: Optional[str] = None,
    user: User = Depends(get_current_user)
):
    return await get_all_leads(session, user, skip, limit, search, lead_type)


@router.get("/{lead_id}", response_model=LeadOut)
async def get_lead(
    lead_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user)
):
    return await get_lead_by_id(session, lead_id)


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