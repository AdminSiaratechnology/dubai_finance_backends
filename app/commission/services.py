from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.commission.models import Bank, LoanType,BankCategory
from app.commission.schemas import LoanCreate,LoanTypeOut,LoanStatus,CategoryCreate,CategoryOut,BankBase,BankCreate
from typing import Optional
from sqlalchemy.orm import selectinload

################# Loan Type ###################
async def create_loan_type(session: AsyncSession, loantype:LoanCreate) -> LoanTypeOut:
  # 🔎 Check if already exists
  result = await session.execute(
    select(LoanType).where(LoanType.name == loantype.name)
  )
  existing_loantype = result.scalar_one_or_none()
  if existing_loantype:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan type already exists"
        )
  loantype = LoanType(name=loantype.name,status=loantype.status,description=loantype.description)
  session.add(loantype)
  await session.commit()
  await session.refresh(loantype)
  return loantype



async def get_all_loan_type(
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
        filters.append(LoanType.name.ilike(f"%{search.strip()}%"))

    # 🔹 Status filter
    if status:
        filters.append(LoanType.status == status)

    # ✅ Total count
    count_stmt = select(func.count(LoanType.id)).where(*filters)
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
        select(LoanType)
        .where(*filters)
        .order_by(LoanType.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)
    items = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items,
    }



################# Get Loan Type By ID ###################

async def get_loan_type_by_id(
    session: AsyncSession,
    loan_type_id: int
) -> LoanTypeOut:

    stmt = select(LoanType).where(LoanType.id == loan_type_id)
    result = await session.execute(stmt)
    loan_type = result.scalar_one_or_none()

    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan type not found"
        )

    return loan_type



################# Update Loan Type ###################

async def update_loan_type(
    session: AsyncSession,
    loan_type_id: int,
    loantype_data: LoanCreate
) -> LoanTypeOut:

    stmt = select(LoanType).where(LoanType.id == loan_type_id)
    result = await session.execute(stmt)
    loan_type = result.scalar_one_or_none()

    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan type not found"
        )

    # 🔎 Check duplicate name (excluding current record)
    duplicate_stmt = select(LoanType).where(
        LoanType.name == loantype_data.name,
        LoanType.id != loan_type_id
    )
    duplicate_result = await session.execute(duplicate_stmt)
    existing = duplicate_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan type with this name already exists"
        )

    # ✅ Update fields
    loan_type.name = loantype_data.name
    loan_type.status = loantype_data.status
    loan_type.description = loantype_data.description

    await session.commit()
    await session.refresh(loan_type)

    return loan_type



################# Bank Category ###################

# from app.commission.models import BankCategory
# from app.commission.schemas import CategoryCreate, CategoryOut


# ✅ Create Category
async def create_category(
    session: AsyncSession,
    category: CategoryCreate
) -> CategoryOut:

    # 🔎 Check duplicate
    result = await session.execute(
        select(BankCategory).where(BankCategory.name == category.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists"
        )

    new_category = BankCategory(
        name=category.name,
        description=category.description,
        status=category.status
    )

    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)

    return new_category


# ✅ Get All Categories (Pagination + Search + Status)
async def get_all_categories(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[LoanStatus] = LoanStatus.active
):

    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []

    # 🔎 Search
    if search:
        filters.append(
            BankCategory.name.ilike(f"%{search.strip()}%")
        )

    # 🔹 Status filter
    if status:
        filters.append(BankCategory.status == status)

    # ✅ Count
    count_stmt = select(func.count(BankCategory.id)).where(*filters)
    total = (await session.execute(count_stmt)).scalar_one()

    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": [],
        }

    # ✅ Data Query
    stmt = (
        select(BankCategory)
        .where(*filters)
        .order_by(BankCategory.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)
    items = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items,
    }


# ✅ Get Category By ID
async def get_category_by_id(
    session: AsyncSession,
    category_id: int
) -> CategoryOut:

    stmt = select(BankCategory).where(BankCategory.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    return category


# ✅ Update Category
async def update_category(
    session: AsyncSession,
    category_id: int,
    category_data: CategoryCreate
) -> CategoryOut:

    stmt = select(BankCategory).where(BankCategory.id == category_id)
    result = await session.execute(stmt)
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )

    # 🔎 Duplicate check (exclude current)
    duplicate_stmt = select(BankCategory).where(
        BankCategory.name == category_data.name,
        BankCategory.id != category_id
    )
    duplicate_result = await session.execute(duplicate_stmt)
    existing = duplicate_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category with this name already exists"
        )

    # ✅ Update fields
    category.name = category_data.name
    category.description = category_data.description
    category.status = category_data.status

    await session.commit()
    await session.refresh(category)

    return category







# ------------------------------Bank-------------------------------------------- 



# 🔹 Create Bank
async def create_bank(session: AsyncSession, bank_data: BankCreate):

    # Check duplicate short_code
    existing = await session.execute(
        select(Bank).where(Bank.short_code == bank_data.short_code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Short code already exists"
        )

    bank = Bank(
        name=bank_data.name,
        short_code=bank_data.short_code,
        default_tat_days=bank_data.default_tat_days,
        description=bank_data.description,
        status=bank_data.status,
        logo_url=bank_data.logo_url,
        category_id=bank_data.category_id
    )

    # Attach Loan Types
    if bank_data.loan_type_ids:
        result = await session.execute(
            select(LoanType).where(LoanType.id.in_(bank_data.loan_type_ids))
        )
        bank.loan_types = list(result.scalars().all())

    session.add(bank)
    await session.commit()
    await session.refresh(bank)

    return bank


# 🔹 Get All Banks
async def get_all_banks(session: AsyncSession):
    result = await session.execute(
        select(Bank).options(
            selectinload(Bank.loan_types),
            selectinload(Bank.category)
        )
    )
    return result.scalars().all()


# 🔹 Get Single Bank
async def get_bank_by_id(session: AsyncSession, bank_id: int):
    result = await session.execute(
        select(Bank)
        .where(Bank.id == bank_id)
        .options(
            selectinload(Bank.loan_types),
            selectinload(Bank.category)
        )
    )

    bank = result.scalar_one_or_none()

    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    return bank


# 🔹 Update Bank
async def update_bank(session: AsyncSession, bank_id: int, bank_data: BankUpdate):

    bank = await get_bank_by_id(session, bank_id)

    update_data = bank_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key != "loan_type_ids":
            setattr(bank, key, value)

    # Update Loan Types
    if bank_data.loan_type_ids is not None:
        result = await session.execute(
            select(LoanType).where(LoanType.id.in_(bank_data.loan_type_ids))
        )
        bank.loan_types = list(result.scalars().all())

    await session.commit()
    await session.refresh(bank)

    return bank


# 🔹 Delete Bank
async def delete_bank(session: AsyncSession, bank_id: int):
    bank = await get_bank_by_id(session, bank_id)

    await session.delete(bank)
    await session.commit()

    return {"message": "Bank deleted successfully"}