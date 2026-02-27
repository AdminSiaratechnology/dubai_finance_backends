from fastapi import APIRouter, Depends,UploadFile,File,Form,HTTPException,status,Query 
from typing import List, Annotated
from app.account.deps import require_admin,User
from app.db.config import SessionDep
from app.commission.schemas import BankCreate, BankOut, BankUpdate, LoanStatus
from app.commission.services import (
    create_bank,
    get_all_banks,
    get_bank_by_id,
    update_bank,
    delete_bank
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
@router.get("/", response_model=List[BankOut])
async def get_all_banks_api(
    session: SessionDep
):
    return await get_all_banks(session)


# 🔹 Get Single Bank
@router.get("/{bank_id}", response_model=BankOut)
async def get_single_bank_api(
    bank_id: int,
    session: SessionDep
):
    return await get_bank_by_id(session, bank_id)


# 🔹 Update Bank
@router.put("/{bank_id}", response_model=BankOut)
async def update_bank_api(
    bank_id: int,
    bank_data: BankUpdate,
    session: SessionDep
):
    return await update_bank(session, bank_id, bank_data)


# 🔹 Delete Bank
@router.delete("/{bank_id}")
async def delete_bank_api(
    bank_id: int,
    session: SessionDep
):
    return await delete_bank(session, bank_id)