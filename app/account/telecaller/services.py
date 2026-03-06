from app.account.models import User, UserRole, TelecallerProfile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func, or_
from fastapi import HTTPException, status
from app.account.telecaller.schemas import TelecallerCreate, TelecallerOut,TelecallerStatus, TelecallerUpdate
from app.account.services import check_email_exists
from app.account.utils import hash_password
from typing import Optional

async def check_emirates_id_exists(emirates_id: str, db: AsyncSession):
    result = await db.execute(
        select(TelecallerProfile).where(
            TelecallerProfile.emirates_id == emirates_id
        )
    )
    return result.scalar_one_or_none()

async def create_telecaller(
    session: AsyncSession,
    telecaller: TelecallerCreate,
) -> TelecallerOut:

    if await check_email_exists(telecaller.email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    if await check_emirates_id_exists(telecaller.emirates_id, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emirates ID already exists"
        )
    
    try:
        # 2️⃣ create user
        user = User(
            email=telecaller.email,
            password_hash=hash_password(telecaller.password),
            role=UserRole.TELECALLER
        )

        session.add(user)
        await session.flush()   # user.id generate

        # 3️⃣ create telecaller profile
        profile = TelecallerProfile(
            user_id=user.id,
            name=telecaller.name,
            phone=telecaller.phone,
            emirates_id=telecaller.emirates_id,
            nationality=telecaller.nationality,
            experience=telecaller.experience,
            account_holder_name=telecaller.account_holder_name,
            bank_name=telecaller.bank_name,
            account_number=telecaller.account_number,
            iban=telecaller.iban
        )

        session.add(profile)

        await session.commit()

        return TelecallerOut(
            id=user.id,
            name=telecaller.name,
            email=user.email,
            phone=profile.phone,
            emirates_id=profile.emirates_id,
            nationality=profile.nationality,
            experience=profile.experience,
            account_holder_name=profile.account_holder_name,
            bank_name=profile.bank_name,
            account_number=profile.account_number,  
            iban=profile.iban,
            status=telecaller.status,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

async def alltelecaller(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None
):
    page = max(page,1)
    limit = max(min(limit, 100), 1)
    filters = []

    if search:
        search= search.strip()
        filters.append(
            or_(
                User.email.ilike(f"%{search}%"),
                TelecallerProfile.phone.ilike(f"%{search}%"),
                TelecallerProfile.account_holder_name.ilike(f"%{search}%")
            )
        )
        
    if status == "active":
        filters.append(User.is_active == True)
    elif status == "inactive":
        filters.append(User.is_active == False)
    
    count_stmt = (
        select(func.count(User.id))
        .join(TelecallerProfile)
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

    stmt = (
        select(User)
        .join(TelecallerProfile)
        .where(*filters)
        .order_by(User.id.desc())
        .offset((page-1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)

    users = result.scalars().all()

    items = []

    for user in users:
        profile = user.telecaller_profile

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

async def get_telecaller_by_id(
    session:AsyncSession,
    telecaller_id: int
):
    stmt = (
        select(User)
        .join(TelecallerProfile)
        .where(
            User.id == telecaller_id,
            User.role == UserRole.TELECALLER
        )
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Telecaller not found"
        )

    profile = user.telecaller_profile

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

async def update_telecaller(
    session: AsyncSession,
    telecaller_id: int,
    data: TelecallerUpdate
):

    stmt = (
        select(User)
        .join(TelecallerProfile)
        .where(
            User.id == telecaller_id,
            User.role == UserRole.TELECALLER
        )
    )

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Coordinator not found"
        )
    profile = user.telecaller_profile

    if data.email != user.email:
        if await check_email_exists(data.email, session):
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )
    
    emirates_check = await session.execute(
        select(TelecallerProfile).where(
            TelecallerProfile.emirates_id == data.emirates_id,
            TelecallerProfile.user_id != telecaller_id
        )
    )

    if emirates_check.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Emirates ID already exists"
        )
        
    user.email = data.email

    if data.status == "active":
        user.is_active = True
    else:
        user.is_active = False

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

async def delete_telecaller(
    session: AsyncSession,
    telecaller_id: int
):

    stmt= select(User).where(
        User.id == telecaller_id,
        User.role == UserRole.TELECALLER
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Telecaller not found"
        )

    await session.delete(user)

    await session.commit()

    return {
        "message": "Telecaller deleted successfully"
    }