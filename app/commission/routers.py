from fastapi import APIRouter, Depends,UploadFile,File,Form,HTTPException,status,Query 
from typing import List, Annotated, Optional
from app.account.deps import require_admin,User
from app.db.config import SessionDep
from app.commission.schemas import CommissionOut,CommissionCreate, PaginatedCommissionOut,CommissionStatus,CommissionUpdate
from app.commission.services import (
    commission_create,
    get_all_commission,
    get_commission_by_id,
    update_commission_service,
    delete_commission_service,
    get_commission_by_bank_and_bankProduct
)


router = APIRouter()


# Create Commission

@router.post("", response_model=CommissionOut)
async def create_commission(
    session: SessionDep,
    commission: CommissionCreate,
    admin_user: User = Depends(require_admin)

):
    return await commission_create(session, commission)

# fetch all data
@router.get("", response_model=PaginatedCommissionOut)
async def commission_list(
    session : SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),
    status: Optional[CommissionStatus] = Query(
        None,   # 👈 changed from LoanStatus.active
        description="Filter by loan status"
    ),
    admin_user: User = Depends(require_admin)
):
    return await get_all_commission(session, page, limit, search, status)

# single data fetch
@router.get("/{commission_id}", response_model=CommissionOut)
async def get_commission(
    commission_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_commission_by_id(session, commission_id)


# Update data
@router.put("/{commission_id}", response_model=CommissionOut)
async def update_commission(
    commission_id: int,
    payload: CommissionUpdate,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await update_commission_service(session, commission_id, payload)

# Delete data
@router.delete("/{commission_id}")
async def delete_commission(
    commission_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await delete_commission_service(session, commission_id)

@router.get("/bank/{bank_id}/product/{product_id}", response_model=CommissionOut)
async def get_commission_by_bank_and_product(
    bank_id: int,
    product_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_commission_by_bank_and_bankProduct(session, bank_id, product_id)