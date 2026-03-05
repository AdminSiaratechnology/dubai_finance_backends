from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.Bank.schemas import BankBase,BankCreate,BankUpdate
from app.Bank.models import Bank
from sqlalchemy import select, func, and_, or_
from app.loantype.models import LoanType
from app.category.models import BankCategory
from app.loantype.schemas import LoanStatus
from typing import Optional
from app.loantype.utils import save_upload_file
from app.product.models import Product
# ------------------------------Bank-------------------------------------------- 



async def create_bank(
    session: AsyncSession,
    bank_data: BankCreate,
    image_url: UploadFile | None = None
) -> Bank:

    # 🔹 Normalize short_code
    bank_data.short_code = bank_data.short_code.lower()

    # =====================================================
    # 🔹 Duplicate Check
    # =====================================================
    existing_stmt = select(Bank).where(
        or_(
            Bank.name == bank_data.name,
            Bank.short_code == bank_data.short_code
        )
    )

    result = await session.execute(existing_stmt)
    existing_bank = result.scalar_one_or_none()

    if existing_bank:
        if existing_bank.name == bank_data.name:
            raise HTTPException(400, "Bank name already exists")
        if existing_bank.short_code == bank_data.short_code:
            raise HTTPException(400, "Short code already exists")

    # =====================================================
    # 🔹 Category Validation
    # =====================================================
    if bank_data.category_id:
        category_result = await session.execute(
            select(BankCategory).where(
                BankCategory.id == bank_data.category_id
            )
        )
        if not category_result.scalar_one_or_none():
            raise HTTPException(400, "Invalid category_id")

    # =====================================================
    # 🔹 Save Image
    # =====================================================
    image_path = None
    if image_url:
        image_path = await save_upload_file(image_url, "companylogo")

    # =====================================================
    # 🔹 Loan Type Validation
    # =====================================================
    loan_types = []
    if bank_data.loan_type_ids:
        loan_type_result = await session.execute(
            select(LoanType).where(
                LoanType.id.in_(bank_data.loan_type_ids)
            )
        )

        loan_types = loan_type_result.scalars().all()

        found_ids = {lt.id for lt in loan_types}
        invalid_ids = set(bank_data.loan_type_ids) - found_ids

        if invalid_ids:
            raise HTTPException(
                400,
                f"Invalid loan type id(s): {list(invalid_ids)}"
            )

    # =====================================================
    # 🔹 Create Bank
    # =====================================================
    bank_dict = bank_data.model_dump(exclude={"loan_type_ids"})

    new_bank = Bank(
        **bank_dict,
        logo_url=image_path,
        loan_types=loan_types
    )

    session.add(new_bank)
    await session.commit()

    # =====================================================
    # 🔹 Re-fetch with eager loading (VERY IMPORTANT)
    # =====================================================
    result = await session.execute(
        select(Bank).where(Bank.id == new_bank.id)
    )

    created_bank = result.scalar_one()
    return created_bank

   




# 🔹 Get All Banks


async def get_all_banks(
    
        session: AsyncSession,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[LoanStatus] = LoanStatus.active  # new
    ):
    # Safety checks
    page = max(page, 1)
    limit = max(min(limit, 100), 1)
    filters = []
     # 🔎 Search filter
    if search:
        filters.append(Bank.name.ilike(f"%{search.strip()}%"))
    # 🔹 Status filter
    if status:
        filters.append(Bank.status == status)
     # ✅ Total count
    count_stmt = select(func.count(Bank.id)).where(*filters)
    total = (await session.execute(count_stmt)).scalar_one()
    # Early return if no data
    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": [],
        }


     # ✅ Main query with ordering & pagination
    stmt = (
        select(Bank)
        .where(*filters)
        .order_by(Bank.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await session.execute(stmt)
   
    
    banks = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": banks,
    }



# 🔹 Get Single Bank
async def get_bank_by_id(session: AsyncSession, bank_id: int):
    result = await session.execute(
        select(Bank).where(Bank.id == bank_id)
    )


    bank = result.scalar_one_or_none()

    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    return bank


# 🔹 Update Bank

async def update_bank(
    session: AsyncSession,
    bank_id: int,
    bank_data: BankCreate,
    image_url: UploadFile | None = None
) -> Bank:

    
    result = await session.execute(
        select(Bank).where(Bank.id == bank_id)
    )
    bank = result.scalar_one_or_none()

    if not bank:
        raise HTTPException(404, "Bank not found")

    # 🔹 Normalize short_code
    bank_data.short_code = bank_data.short_code.lower()

    # 🔹 Unique validation (exclude current bank)
    existing_stmt = select(Bank).where(
        or_(
            Bank.name == bank_data.name,
            Bank.short_code == bank_data.short_code
        ),
        Bank.id != bank_id
    )
    result = await session.execute(existing_stmt)
    existing_bank = result.scalar_one_or_none()

    if existing_bank:
        if existing_bank.name == bank_data.name:
            raise HTTPException(400, "Bank name already exists")
        if existing_bank.short_code == bank_data.short_code:
            raise HTTPException(400, "Short code already exists")

    # 🔹 Category validation
    if bank_data.category_id:
        category_result = await session.execute(
            select(BankCategory).where(
                BankCategory.id == bank_data.category_id
            )
        )
        category = category_result.scalar_one_or_none()
        if not category:
            raise HTTPException(400, "Invalid category_id")

    # 🔹 Loan type validation
    loan_types = []
    if bank_data.loan_type_ids:
        loan_type_result = await session.execute(
            select(LoanType).where(
                LoanType.id.in_(bank_data.loan_type_ids)
            )
        )
        loan_types = loan_type_result.scalars().all()

        if len(loan_types) != len(set(bank_data.loan_type_ids)):
            raise HTTPException(400, "Invalid loan type id")

    # 🔹 Update Image (if provided)
    if image_url:
        image_path = await save_upload_file(image_url, "companylogo")
        bank.logo_url = image_path

    # 🔹 Update fields
    bank.name = bank_data.name
    bank.short_code = bank_data.short_code
    bank.default_tat_days = bank_data.default_tat_days
    bank.description = bank_data.description
    bank.status = bank_data.status
    bank.category_id = bank_data.category_id

    # 🔹 Update loan types (replace old)
    bank.loan_types = loan_types

    await session.commit()
    await session.refresh(bank)

    return bank

# 🔹 Delete Bank
async def delete_bank(session: AsyncSession, bank_id: int):
    bank = await get_bank_by_id(session, bank_id)

    await session.delete(bank)
    await session.commit()

    return {"message": "Bank deleted successfully"}


# product show bank id wise
async def get_products_by_bank_service(
    session: AsyncSession,
    bank_id: int
):

    query = (
        select(Product.id, Product.product_name)
        .where(Product.bank_id == bank_id)
        .order_by(Product.product_name)
    )

    result = await session.execute(query)

    products = result.all()

    return [
        {
            "id": p.id,
            "product_name": p.product_name
        }
        for p in products
    ]