from app.account.models import User, UserRole, CoordinatorProfile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, or_
from fastapi import HTTPException, status
from app.account.analyst.schemas import CoordinatorCreate, CoordinatorOut,CoordinatorStatus
from app.account.services import check_email_exists
from app.account.utils import hash_password
from typing import Optional

async def check_emirates_id_exists(emirates_id: str, db: AsyncSession):
    result = await db.execute(
        select(CoordinatorProfile).where(
            CoordinatorProfile.emirates_id == emirates_id
        )
    )
    return result.scalar_one_or_none()

async def create_coordinator(
    session: AsyncSession,
    coordinator: CoordinatorCreate
) -> CoordinatorOut:

    # 1️⃣ check email exists
    if await check_email_exists(coordinator.email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    # check emirates id
    if await check_emirates_id_exists(coordinator.emirates_id, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emirates ID already exists"
        )

    try:
        # 2️⃣ create user
        user = User(
            email=coordinator.email,
            password_hash=hash_password(coordinator.password),
            role=UserRole.COORDINATOR
        )

        session.add(user)
        await session.flush()   # user.id generate

        # 3️⃣ create coordinator profile
        profile = CoordinatorProfile(
            user_id=user.id,
            name=coordinator.name,
            phone=coordinator.phone,
            emirates_id=coordinator.emirates_id,
            nationality=coordinator.nationality,
            experience=coordinator.experience,
            account_holder_name=coordinator.account_holder_name,
            bank_name=coordinator.bank_name,
            account_number=coordinator.account_number,
            iban=coordinator.iban
        )

        session.add(profile)

        await session.commit()

        return CoordinatorOut(
            id=user.id,
            name=coordinator.name,
            email=user.email,
            phone=profile.phone,
            emirates_id=profile.emirates_id,
            nationality=profile.nationality,
            experience=profile.experience,
            account_holder_name=profile.account_holder_name,
            bank_name=profile.bank_name,
            account_number=profile.account_number,  
            iban=profile.iban,
            status=coordinator.status,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


async def allcoordinator(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None
):

    # ✅ Safety checks
    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []

    # 🔎 Search filter
    if search:
        search = search.strip()

        filters.append(
            or_(
                User.email.ilike(f"%{search}%"),
                CoordinatorProfile.phone.ilike(f"%{search}%"),
                CoordinatorProfile.account_holder_name.ilike(f"%{search}%")
            )
        )

    # 🔹 Status filter
    if status == "active":
        filters.append(User.is_active == True)

    elif status == "inactive":
        filters.append(User.is_active == False)

    # ✅ Total count
    count_stmt = (
        select(func.count(User.id))
        .join(CoordinatorProfile)
        .where(*filters)
    )

    total = (await session.execute(count_stmt)).scalar_one()

    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": []
        }

    # ✅ Main query with pagination
    stmt = (
        select(User)
        .join(CoordinatorProfile)
        .where(*filters)
        .order_by(User.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)

    users = result.scalars().all()

    items = []

    for user in users:
        profile = user.coordinator_profile

        items.append({
            "id": user.id,
            "name": profile.account_holder_name if profile else None,
            "email": user.email,
            "phone": profile.phone if profile else None,
            "emirates_id": profile.emirates_id if profile else None,
            "nationality": profile.nationality if profile else None,
            "experience": profile.experience if profile else None,
            "account_holder_name": profile.account_holder_name if profile else None,
            "bank_name": profile.bank_name if profile else None,
            "account_number": profile.account_number if profile else None,
            "iban": profile.iban if profile else None,
            "status": "active" if user.is_active else "inactive",
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }




async def get_coordinator_by_id(
    session: AsyncSession,
    coordinator_id: int
):

    stmt = (
        select(User)
        .join(CoordinatorProfile)
        .where(
            User.id == coordinator_id,
            User.role == UserRole.COORDINATOR
        )
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coordinator not found"
        )

    profile = user.coordinator_profile

    return {
        "id": user.id,
        "name": profile.account_holder_name if profile else None,
        "email": user.email,
        "phone": profile.phone if profile else None,
        "emirates_id": profile.emirates_id if profile else None,
        "nationality": profile.nationality if profile else None,
        "experience": profile.experience if profile else None,
        "account_holder_name": profile.account_holder_name if profile else None,
        "bank_name": profile.bank_name if profile else None,
        "account_number": profile.account_number if profile else None,
        "iban": profile.iban if profile else None,
        "status": "active" if user.is_active else "inactive",
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }



from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.account.models import User, CoordinatorProfile, UserRole
from app.account.services import check_email_exists
from app.account.analyst.schemas import CoordinatorUpdate


async def update_coordinator(
    session: AsyncSession,
    coordinator_id: int,
    data:CoordinatorUpdate
):

    stmt = (
        select(User)
        .join(CoordinatorProfile)
        .where(
            User.id == coordinator_id,
            User.role == UserRole.COORDINATOR
        )
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Coordinator not found"
        )

    profile = user.coordinator_profile

    # 🔹 Email duplicate check
    if data.email != user.email:
        if await check_email_exists(data.email, session):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    # 🔹 Emirates ID duplicate check
    emirates_check = await session.execute(
        select(CoordinatorProfile).where(
            CoordinatorProfile.emirates_id == data.emirates_id,
            CoordinatorProfile.user_id != coordinator_id
        )
    )

    if emirates_check.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Emirates ID already exists"
        )

    # ---------------- USER UPDATE ----------------

    user.email = data.email

    if data.status == "active":
        user.is_active = True
    else:
        user.is_active = False

    # ---------------- PROFILE UPDATE ----------------

    profile.name = data.name
    profile.phone = data.phone
    profile.emirates_id = data.emirates_id
    profile.nationality = data.nationality
    profile.experience = data.experience
    profile.account_holder_name = data.account_holder_name
    profile.bank_name = data.bank_name
    profile.account_number = data.account_number
    profile.iban = data.iban

    await session.commit()

    await session.refresh(user)

    return {
        "id": user.id,
        "name": data.name,
        "email": user.email,
        "phone": profile.phone,
        "emirates_id": profile.emirates_id,
        "nationality": profile.nationality,
        "experience": profile.experience,
        "account_holder_name": profile.account_holder_name,
        "bank_name": profile.bank_name,
        "account_number": profile.account_number,
        "iban": profile.iban,
        "status": "active" if user.is_active else "inactive",
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }



async def delete_coordinator(
    session: AsyncSession,
    coordinator_id: int
):

    stmt = select(User).where(
        User.id == coordinator_id,
        User.role == UserRole.COORDINATOR
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Coordinator not found"
        )

    await session.delete(user)

    await session.commit()

    return {
        "message": "Coordinator deleted successfully"
    }