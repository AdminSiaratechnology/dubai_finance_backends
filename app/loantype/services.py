from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.loantype.models import  LoanType
from app.loantype.schemas import LoanCreate,LoanTypeOut,LoanStatus
from typing import Optional



################# Loan Type ######################################################

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
    status: Optional[LoanStatus] = None  # 👈 changed
):
    # Safety checks
    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []

    # 🔎 Search filter
    if search and search.strip():
        filters.append(LoanType.name.ilike(f"%{search.strip()}%"))

    # 🔹 Status filter (only if provided)
    if status is not None:
        filters.append(LoanType.status == status)

    # ✅ Total count
    count_stmt = select(func.count()).select_from(LoanType)

    if filters:
        count_stmt = count_stmt.where(*filters)

    total = (await session.execute(count_stmt)).scalar_one()

    # Early return
    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": [],
        }

    # ✅ Main query
    stmt = select(LoanType)

    if filters:
        stmt = stmt.where(*filters)

    stmt = (
        stmt.order_by(LoanType.id.desc())
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


# Delete Loan Type
async def delete_loan_type(
    session: AsyncSession,
    loan_type_id: int
):
    loan_type = await get_loan_type_by_id(session, loan_type_id)

    await session.delete(loan_type)
    await session.commit()

    return {"message": "Loan type deleted successfully"}
