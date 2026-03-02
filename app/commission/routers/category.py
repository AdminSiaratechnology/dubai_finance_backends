from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.account.deps import require_admin
from app.account.models import User
from app.db.config import SessionDep
from app.commission.schemas import (
    CategoryCreate,
    CategoryOut,
    PaginatedProductOut,
    LoanStatus
)
from app.commission.services import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category
)

router = APIRouter()


# ✅ Create Category
@router.post("", response_model=CategoryOut)
async def category_create(
    session: SessionDep,
    category: CategoryCreate,
    admin_user: User = Depends(require_admin)
):
    return await create_category(session, category)


# ✅ Get All Categories
@router.get("", response_model=PaginatedProductOut)
async def category_list(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(10, le=100),
    search: Optional[str] = None,
    status: Optional[LoanStatus] = Query(
        None,   # 👈 changed from LoanStatus.active
        description="Filter by loan status"
    ),
    admin_user: User = Depends(require_admin)
):
    return await get_all_categories(
        session,
        page,
        limit,
        search,
        status
    )


# ✅ Get Category By ID
@router.get("/{category_id}", response_model=CategoryOut)
async def category_detail(
    category_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_category_by_id(session, category_id)


# ✅ Update Category
@router.put("/{category_id}", response_model=CategoryOut)
async def category_update(
    category_id: int,
    category: CategoryCreate,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await update_category(
        session,
        category_id,
        category
    )


# Delete Category
@router.delete("/{category_id}")
async def category_delete(
    category_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)   
):
    result = await delete_category(session, category_id)
    if not result:
        raise HTTPException(status_code=404, detail="Category not found")
    