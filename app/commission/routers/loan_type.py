from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.commission.schemas import LoanCreate,LoanTypeOut,PaginatedProductOut,LoanStatus
from app.commission.services import create_loan_type,get_all_loan_type
from typing import Optional
router = APIRouter()


@router.post("/loantype", response_model=LoanTypeOut)
async def loan_type_create(session: SessionDep, loantypecreate: LoanCreate, admin_user: User = Depends(require_admin)):
  return await create_loan_type(session, loantypecreate)


@router.get("/loantype", response_model=PaginatedProductOut)
async def list_loantype(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),
    status: Optional[LoanStatus] = Query(LoanStatus.active, description="Filter by loan status")
):
    return await get_all_loan_type(session, page, limit, search, status)