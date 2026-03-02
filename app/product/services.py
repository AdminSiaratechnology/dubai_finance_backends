from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.schemas import ProductOut, ProductCreate
from sqlalchemy import select, func, and_, or_
from app.product.models import Product
from app.commission.models import Bank, LoanType
from app.sla_template.models import SLATemplate


# ✅ Create Product
async def product_create(
    session: AsyncSession,
    product: ProductCreate
) -> Product:

    # 🔎 1️⃣ Check Bank Exists
    bank_result = await session.execute(
        select(Bank).where(Bank.id == product.bank_id)
    )
    bank = bank_result.scalar_one_or_none()

    if not bank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid bank_id"
        )

    # 🔎 2️⃣ Check Loan Type Exists
    loan_type_result = await session.execute(
        select(LoanType).where(LoanType.id == product.loan_type_id)
    )
    loan_type = loan_type_result.scalar_one_or_none()

    if not loan_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid loan_type_id"
        )

    # 🔎 3️⃣ Check SLA Template Exists
    sla_result = await session.execute(
        select(SLATemplate).where(SLATemplate.id == product.sla_template_id)
    )
    sla = sla_result.scalar_one_or_none()

    if not sla:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid sla_template_id"
        )

    # 🔎 4️⃣ Check Duplicate Product (same bank + product name)
    duplicate_result = await session.execute(
        select(Product).where(
            Product.product_name == product.product_name,
            Product.bank_id == product.bank_id
        )
    )
    existing = duplicate_result.scalar_one_or_none()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists for this bank"
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
    await session.refresh(new_product)

    return new_product