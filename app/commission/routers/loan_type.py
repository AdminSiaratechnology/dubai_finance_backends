from fastapi import APIRouter, Depends, HTTPException, status
from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.commission.schemas import LoanCreate,LoanTypeOut

router = APIRouter()


# @router.post("/", response_model=LoanTypeOut)
# async def category_create(session: SessionDep, category: CategoryCreate, admin_user: User = Depends(require_admin)):
#   return await create_category(session, category)
