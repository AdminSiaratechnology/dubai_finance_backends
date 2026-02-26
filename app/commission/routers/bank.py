from fastapi import APIRouter, Depends
from typing import List

from app.db.config import SessionDep
from app.commission.schemas import BankCreate, BankOut, BankUpdate
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
async def create_bank_api(
    bank_data: BankCreate,
    session: SessionDep
):
    return await create_bank(session, bank_data)


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