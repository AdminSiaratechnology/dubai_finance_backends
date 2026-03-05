
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.commission.schemas import CommissionCreate
from app.commission.models import Commission
from app.Bank.models import Bank
from app.product.models import Product
from sqlalchemy import select, func, or_
from typing import Optional
from app.commission.schemas import CommissionStatus,CommissionUpdate

# Create Commission
async def commission_create(
    session: AsyncSession,
    commission: CommissionCreate,
        
) -> Commission:
    # 🔎 1️⃣ Validate Bank
    bank_result = await session.execute(
        select(Bank).where(Bank.id == commission.bank_id)
    )
    if not bank_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bank_id"
        )
     # 🔎 1️⃣ Validate Product
    product_result = await session.execute(
        select(Product).where(Product.id == commission.product_id)
    )
    if not product_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid product_id"
        )
    # 🔎  Duplicate check (same bank + name + product)
    duplicate_result = await session.execute(
        select(Commission).where(
            Commission.bank_id == commission.bank_id,
            Commission.product_id == commission.product_id,
        )
    )
    if duplicate_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Commission already exists for this bank and Product"
        )
    
    # 🔎 Commission Share Validation
    total_share = (
        (commission.agent_share or 0) +
        (commission.telecaller_share or 0) +
        (commission.coordinator_share or 0)
    )

    if total_share > commission.commission_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Total share (agent + telecaller + coordinator) cannot exceed commission value"
        )
    
    # Create Commission

    new_commission = Commission(
        bank_id = commission.bank_id,
        product_id = commission.product_id,
        commission_type = commission.commission_type,
        commission_value = commission.commission_value,
        agent_share = commission.agent_share,
        telecaller_share = commission.telecaller_share,
        coordinator_share = commission.coordinator_share,
        effective_from_date = commission.effective_from_date,
        status = commission.status

    )
    session.add(new_commission)
    await session.commit()
     # refresh to load relationships
    await session.refresh(new_commission)
    return new_commission


# get all commission 



async def get_all_commission(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[CommissionStatus] = None
):

    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []
    joins_required = False

    # Status filter
    if status:
        filters.append(Commission.status == status)

    # Search filter
    if search and search.strip():
        joins_required = True
        search_term = f"%{search.strip().lower()}%"

        filters.append(
            or_(
                func.lower(Bank.name).like(search_term),
                func.lower(Product.product_name).like(search_term)
            )
        )

    # ---------- COUNT QUERY ----------
    count_query = select(func.count()).select_from(Commission)

    if joins_required:
        count_query = (
            count_query
            .join(Bank, Commission.bank_id == Bank.id)
            .join(Product, Commission.product_id == Product.id)
        )

    if filters:
        count_query = count_query.where(*filters)

    total_result = await session.execute(count_query)
    total = total_result.scalar_one()

    # ---------- DATA QUERY ----------
    query = select(Commission)

    if joins_required:
        query = (
            query
            .join(Bank, Commission.bank_id == Bank.id)
            .join(Product, Commission.product_id == Product.id)
        )

    if filters:
        query = query.where(*filters)

    query = (
        query
        .order_by(Commission.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(query)
    commissions = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": commissions
    }


# Single Fetch Data 
async def get_commission_by_id(
    session: AsyncSession,
    commission_id: int
):

    query = select(Commission).where(Commission.id == commission_id)

    result = await session.execute(query)
    commission = result.scalar_one_or_none()

    if not commission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )

    return commission


# Update data
from sqlalchemy import select
from fastapi import HTTPException, status

async def update_commission_service(
    session: AsyncSession,
    commission_id: int,
    payload: CommissionUpdate
):

    # Get existing commission
    query = select(Commission).where(Commission.id == commission_id)
    result = await session.execute(query)
    commission = result.scalar_one_or_none()

    if not commission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )

    # Only update provided fields
    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(commission, field, value)

    await session.commit()
    await session.refresh(commission)

    return commission


# Delete Data
async def delete_commission_service(
    session: AsyncSession,
    commission_id: int
):

    query = select(Commission).where(Commission.id == commission_id)
    result = await session.execute(query)
    commission = result.scalar_one_or_none()

    if not commission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Commission not found"
        )

    await session.delete(commission)
    await session.commit()

    return {
        "message": "Commission deleted successfully"
    }