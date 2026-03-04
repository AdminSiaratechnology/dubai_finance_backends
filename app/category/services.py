
from sqlalchemy.ext.asyncio import AsyncSession
from app.category.schemas import CategoryCreate,CategoryOut
from app.category.models import BankCategory
from sqlalchemy import select, func, and_, or_
from fastapi import HTTPException, status
from typing import Optional
from app.loantype.schemas import LoanStatus
################# Bank Category ###################


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
    # status: Optional[LoanStatus] = LoanStatus.active
    status: Optional[LoanStatus] = None 
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




# ✅ Delete Category
async def delete_category(
    session: AsyncSession,
    category_id: int
):
    category = await get_category_by_id(session, category_id)

    await session.delete(category)
    await session.commit()

    return {"message": "Category deleted successfully"}


