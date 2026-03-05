from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.schemas import ProductOut, ProductCreate, ProductStatus
from sqlalchemy import select, func, and_, or_
from app.product.models import Product
from app.Bank.models import Bank
from app.loantype.models import LoanType
from app.sla_template.models import SLATemplate
from typing import Optional
from sqlalchemy.orm import selectinload




async def product_create(
    session: AsyncSession,
    product: ProductCreate
) -> Product:

    # 🔎 1️⃣ Validate Bank
    bank_result = await session.execute(
        select(Bank).where(Bank.id == product.bank_id)
    )
    if not bank_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bank_id"
        )

    # 🔎 2️⃣ Validate Loan Type
    loan_type_result = await session.execute(
        select(LoanType).where(LoanType.id == product.loan_type_id)
    )
    if not loan_type_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan_type_id"
        )

    # 🔎 3️⃣ Validate SLA Template (nullable handle)
    if product.sla_template_id:
        sla_result = await session.execute(
            select(SLATemplate).where(
                SLATemplate.id == product.sla_template_id
            )
        )
        if not sla_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sla_template_id"
            )

    # 🔎 4️⃣ Duplicate check (same bank + name + loan type)
    duplicate_result = await session.execute(
        select(Product).where(
            Product.product_name == product.product_name,
            Product.bank_id == product.bank_id,
            Product.loan_type_id == product.loan_type_id,
        )
    )
    if duplicate_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists for this bank and loan type"
        )

    # ✅ Create Product
    new_product = Product(
        product_name=product.product_name,
        customer_segment=product.customer_segment,
        bank_id=product.bank_id,
        loan_type_id=product.loan_type_id,
        sla_template_id=product.sla_template_id,
        min_loan_amount=product.min_loan_amount,
        max_loan_amount=product.max_loan_amount,
        min_tenure=product.min_tenure,
        max_tenure=product.max_tenure,
        processing_fee=product.processing_fee,
        priority_score=product.priority_score,
        internal_notes=product.internal_notes,
        status=product.status,
    )

    session.add(new_product)
    await session.commit()

    # 🔥 Re-fetch with relationships (VERY IMPORTANT)
    stmt = (
        select(Product)
        .options(
            selectinload(Product.bank),
            selectinload(Product.loan_type),
            selectinload(Product.sla_template),
        )
        .where(Product.id == new_product.id)
    )

    result = await session.execute(stmt)
    created_product = result.scalar_one()

    return created_product



# 🔹 Get All Banks


async def get_all_products(
    
        session: AsyncSession,
        page: int = 1,
        limit: int = 10,
        search: Optional[str] = None,
        status: Optional[ProductStatus] = None
    ):
    # Safety checks
    page = max(page, 1)
    limit = max(min(limit, 100), 1)
    filters = []
     # 🔎 Search filter
    if search:
        filters.append(Product.product_name.ilike(f"%{search.strip()}%"))
    # 🔹 Status filter
    if status:
        filters.append(Product.status == status)
     # ✅ Total count
    count_stmt = select(func.count(Product.id)).where(*filters)
    total = (await session.execute(count_stmt)).scalar_one()
    # Early return if no data
    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": [],
        }


     
    stmt = (
    select(Product)
    .options(
        selectinload(Product.bank),
        selectinload(Product.loan_type),
        selectinload(Product.sla_template),
    )
    .where(*filters)
    .order_by(Product.id.desc())
    .offset((page - 1) * limit)
    .limit(limit)
)
    result = await session.execute(stmt)
   
    
    products = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": products,
    }



async def get_product_by_id(
    session: AsyncSession,
    product_id: int,
) -> Optional[ProductOut]:

    stmt = (
        select(Product)
        .options(
            selectinload(Product.bank),
            selectinload(Product.loan_type),
            selectinload(Product.sla_template),
        )
        .where(Product.id == product_id)
    )

    result = await session.execute(stmt)
    product = result.scalar_one_or_none()

    return product



# --------------------------------------- PUt --------------------    



# ✅ Update product

async def update_product(
    session: AsyncSession,
    product_id: int,
    product_data: ProductCreate
)-> ProductOut:

    # 🔎 Check if product exists
    # stmt = select(Product).where(Product.id == product_id)
    stmt = (
    select(Product)
    .options(
        selectinload(Product.bank),
        selectinload(Product.loan_type),
        selectinload(Product.sla_template),
    )
    .where(Product.id == product_id)
)
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # 🔎 Validate Bank
    bank_stmt = select(Bank).where(Bank.id == product_data.bank_id)
    bank_result = await session.execute(bank_stmt)
    if not bank_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bank_id"
        )

    # 🔎 Validate Loan Type
    loan_stmt = select(LoanType).where(LoanType.id == product_data.loan_type_id)
    loan_result = await session.execute(loan_stmt)
    if not loan_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan_type_id"
        )

    # 🔎 Validate SLA Template (nullable field)
    if product_data.sla_template_id:
        sla_stmt = select(SLATemplate).where(
            SLATemplate.id == product_data.sla_template_id
        )
        sla_result = await session.execute(sla_stmt)
        if not sla_result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid sla_template_id"
            )

    # 🔎 Duplicate check
    duplicate_stmt = select(Product).where(
        Product.product_name == product_data.product_name,
        Product.bank_id == product_data.bank_id,
        Product.loan_type_id == product_data.loan_type_id,
        Product.id != product_id
    )
    duplicate_result = await session.execute(duplicate_stmt)
    existing = duplicate_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this name already exists"
        )

    # ✅ Update fields
    product.product_name = product_data.product_name
    product.customer_segment = product_data.customer_segment
    product.min_loan_amount = product_data.min_loan_amount
    product.max_loan_amount = product_data.max_loan_amount
    product.min_tenure = product_data.min_tenure
    product.max_tenure = product_data.max_tenure
    product.processing_fee = product_data.processing_fee
    product.priority_score = product_data.priority_score
    product.internal_notes = product_data.internal_notes
    product.status = product_data.status

    product.bank_id = product_data.bank_id
    product.loan_type_id = product_data.loan_type_id
    product.sla_template_id = product_data.sla_template_id

    await session.commit()
    await session.refresh(product)

    return product



# ✅ Delete Product
async def delete_product(
    session: AsyncSession,
    product_id: int
):
    product = await get_product_by_id(session, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    await session.delete(product)
    await session.commit()

    return {"message": "Product deleted successfully"}

