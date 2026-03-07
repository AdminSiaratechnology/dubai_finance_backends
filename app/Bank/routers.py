from fastapi import APIRouter, Depends,UploadFile,File,Form,HTTPException,status,Query 
from typing import List, Annotated, Optional
from app.account.deps import require_admin,User
from app.db.config import SessionDep
from app.loantype.schemas import  LoanStatus
from app.Bank.schemas import  BankCreate, BankOut, BankUpdate, PaginatedBankOut
from app.product.schemas import ProductLite

from app.Bank.services import (
    create_bank,
    get_all_banks,
    get_bank_by_id,
    update_bank,
    delete_bank,
    get_products_by_bank_service
)

router = APIRouter()


# 🔹 Create Bank
@router.post("/", response_model=BankOut)
async def bank_create(
    session: SessionDep,
    name: str = Form(...),
    short_code: str = Form(...),
    default_tat_days: int = Form(...),
    description: str | None = Form(None),
    status : LoanStatus = Form(...),
    category_id: int | None = Form(None), 
    loan_type_ids : Annotated[list[int], Form()] = [],
    image: UploadFile | None = File(None),
    admin_user: User = Depends(require_admin)


):
    data = BankCreate(
        name = name,
        short_code = short_code,
        default_tat_days = default_tat_days,
        description = description,
        status = status,
        category_id=category_id,
        loan_type_ids=loan_type_ids
        
    )
    return await create_bank(session, data, image_url = image  )


# 🔹 Get All Banks
@router.get("/", response_model=PaginatedBankOut)
async def get_all_banks_api(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),
    status: Optional[LoanStatus] = Query(LoanStatus.active, description="Filter by loan status"),
    # admin_user: User = Depends(require_admin)
):
    return await get_all_banks(session, page, limit, search, status)


# 🔹 Get Single Bank
@router.get("/{bank_id}", response_model=BankOut)
async def get_single_bank_api(
    bank_id: int,
    session: SessionDep
):
    return await get_bank_by_id(session, bank_id)


# # 🔹 Update Bank
# @router.put("/{bank_id}", response_model=BankOut)
# async def update_bank_api(
#     bank_id: int,
#     bank_data: BankUpdate,
#     session: SessionDep
# ):
#     return await update_bank(session, bank_id, bank_data)


# 🔹 Update Bank
@router.put("/{bank_id}", response_model=BankOut)
async def bank_update(
    bank_id: int,
    session: SessionDep,
    name: str = Form(...),
    short_code: str = Form(...),
    default_tat_days: int = Form(...),
    description: str | None = Form(None),
    status: LoanStatus = Form(...),
    category_id: int | None = Form(None),
    loan_type_ids: Annotated[list[int], Form()] = [],
    image: UploadFile | None = File(None),
    admin_user: User = Depends(require_admin)
):
    data = BankCreate(
        name=name,
        short_code=short_code,
        default_tat_days=default_tat_days,
        description=description,
        status=status,
        category_id=category_id,
        loan_type_ids=loan_type_ids
    )

    return await update_bank(session, bank_id, data, image_url=image)

# 🔹 Delete Bank
@router.delete("/{bank_id}")
async def delete_bank_api(
    bank_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await delete_bank(session, bank_id)


# product show bank id wise
@router.get("/{bank_id}/products", response_model=list[ProductLite])
async def get_products_by_bank(
    bank_id: int,
    session: SessionDep,
    # admin_user: User = Depends(require_admin)
):
    return await get_products_by_bank_service(session, bank_id)