from fastapi import APIRouter, Depends, HTTPException, status
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.commission.schemas import LoanCreate,LoanTypeOut
from app.commission.services import create_loan_type
router = APIRouter()


@router.post("/", response_model=LoanTypeOut)
async def loan_type_create(session: SessionDep, loantypecreate: LoanCreate, admin_user: User = Depends(require_admin)):
  return await create_loan_type(session, loantypecreate)
