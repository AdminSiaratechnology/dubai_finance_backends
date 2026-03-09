from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.account.deps import get_current_user
from app.Lead.SubmitLead.schemas import LeadOut, LeadCreate
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.Lead.SubmitLead.services import submit_lead



router = APIRouter()

# Create Submit Lead
@router.post("", response_model=LeadOut)
async def submit_lead_create(
    session: SessionDep,
    lead_data: LeadCreate,
    user: User = Depends(get_current_user)
):
    return await submit_lead(session, lead_data, user)
