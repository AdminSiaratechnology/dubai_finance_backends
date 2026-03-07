from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from fastapi import HTTPException, status

from app.account.models import User, AgentProfile, UserRole
from app.account.agent.schemas import AgentCreate, AgentStatus, AgentUpdate
from app.commission.models import Commission
from app.account.utils import hash_password
from sqlalchemy.orm import joinedload, selectinload



async def create_agent(session: AsyncSession, agent_data: AgentCreate):

    # ---------------- CHECK EMAIL ----------------
    stmt = select(User).where(User.email == agent_data.email)
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # ---------------- CHECK EMIRATES ID ----------------
    stmt = select(AgentProfile).where(
        AgentProfile.emirates_id == agent_data.emirates_id
    )
    result = await session.execute(stmt)
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Emirates ID already exists"
        )

    # ---------------- CREATE USER ----------------
    new_user = User(
        email=agent_data.email,
        password_hash=hash_password(agent_data.password),
        role=UserRole.AGENT,
    )

    session.add(new_user)
    await session.flush()

    # ---------------- VALIDATE COMMISSIONS ----------------
    commissions = []

    if agent_data.commission_ids:

        stmt = select(Commission).where(
            Commission.id.in_(agent_data.commission_ids)
        )

        result = await session.execute(stmt)
        commissions = result.scalars().all()

        found_ids = {c.id for c in commissions}
        requested_ids = set(agent_data.commission_ids)

        invalid_ids = requested_ids - found_ids

        if invalid_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid commission ids: {list(invalid_ids)}"
            )

    # ---------------- CREATE AGENT PROFILE ----------------
    agent_profile = AgentProfile(
        user_id=new_user.id,
        name=agent_data.name,
        phone=agent_data.phone,
        emirates_id=agent_data.emirates_id,
        nationality=agent_data.nationality,
        business_name=agent_data.bussiness_name,
        year_of_experience=agent_data.year_of_experience,
        account_holder_name=agent_data.account_holder_name,
        bank_name=agent_data.bank_name,
        account_number=agent_data.account_number,
        iban=agent_data.iban,
        commissions=commissions
    )

    session.add(agent_profile)

    await session.commit()
    await session.refresh(agent_profile)

    return {
        "id": agent_profile.id,
        "user_id": new_user.id, 
        "bussiness_name": agent_profile.business_name,
        "name": agent_profile.name,
        "email": new_user.email,
        "phone": agent_profile.phone,
        "emirates_id": agent_profile.emirates_id,
        "nationality": agent_profile.nationality,
        "experience": agent_profile.year_of_experience,
        "account_holder_name": agent_profile.account_holder_name,
        "bank_name": agent_profile.bank_name,
        "account_number": agent_profile.account_number,
        "iban": agent_profile.iban,
        "status": "active",
        "commission_ids": [c.id for c in commissions],
        "created_at": new_user.created_at,
        "updated_at": new_user.updated_at
    }

from typing import Optional




async def get_all_agents(
    session: AsyncSession,
    page: int = 1,
    limit: int = 10,
    search: Optional[str] = None,
    status: Optional[AgentStatus] = None
):

    # 🔹 Safety checks
    page = max(page, 1)
    limit = max(min(limit, 100), 1)

    filters = []

    # 🔎 Search filter
    if search:
        search = search.strip()
        filters.append(
            or_(
                AgentProfile.name.ilike(f"%{search}%"),
                AgentProfile.phone.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
        )

    # 🔹 Status filter (User.is_active)
    if status:
        if status == AgentStatus.active:
            filters.append(User.is_active == True)
        else:
            filters.append(User.is_active == False)

    # 🔢 Total count
    count_stmt = (
        select(func.count(AgentProfile.id))
        .join(User)
        .where(*filters)
    )

    total = (await session.execute(count_stmt)).scalar_one()

    # Early return
    if total == 0:
        return {
            "total": 0,
            "page": page,
            "limit": limit,
            "items": []
        }

    # 🔹 Main query
    stmt = (
        select(AgentProfile)
        .join(User)
        .where(*filters)
        .options(
            joinedload(AgentProfile.user),
            selectinload(AgentProfile.commissions)
            .options(
                selectinload(Commission.bank),
                selectinload(Commission.product),
            )
        )
        .order_by(AgentProfile.id.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    result = await session.execute(stmt)
    agents = result.scalars().all()

    items = []

    for agent in agents:

        user = agent.user

        commissions = []
        for c in agent.commissions:
            commissions.append({
                "id": c.id,
                "commission_type": c.commission_type,
                "commission_value": c.commission_value,
                "effective_from_date": c.effective_from_date,
                "bank": {
                    "id": c.bank.id,
                    "name": c.bank.name
                } if c.bank else None,
                "product": {
                    "id": c.product.id,
                    "product_name": c.product.product_name
                } if c.product else None,
                "created_at": c.created_at,
                "updated_at": c.updated_at
            })

        items.append({
        "id": agent.id,
        "user_id": agent.user_id,
        "bussiness_name": agent.business_name,
        "name": agent.name,
        "email": user.email,
        "phone": agent.phone,
        "emirates_id": agent.emirates_id,
        "nationality": agent.nationality,
        "experience": agent.year_of_experience,
        "account_holder_name": agent.account_holder_name,
        "bank_name": agent.bank_name,
        "account_number": agent.account_number,
        "iban": agent.iban,
        "status": "active" if user.is_active else "inactive",
        "commissions": commissions,   # 👈 change here
        "created_at": user.created_at,
        "updated_at": user.updated_at
    })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }






async def get_agent_by_id(session: AsyncSession, agent_id: int):

    stmt = (
        select(AgentProfile)
        .where(AgentProfile.id == agent_id)
        .options(
            selectinload(AgentProfile.user),
            selectinload(AgentProfile.commissions)
                .selectinload(Commission.bank),
            selectinload(AgentProfile.commissions)
                .selectinload(Commission.product),
        )
    )

    result = await session.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    user = agent.user

    commissions = [
        {
            "id": c.id,
            "commission_type": c.commission_type,
            "commission_value": c.commission_value,
            "effective_from_date": c.effective_from_date,
            "bank": {
                "id": c.bank.id,
                "name": c.bank.name
            } if c.bank else None,
            "product": {
                "id": c.product.id,
                "product_name": c.product.product_name
            } if c.product else None,
            "created_at": c.created_at,
            "updated_at": c.updated_at
        }
        for c in agent.commissions
    ]

    return {
        "id": agent.id,
        "name": agent.name,
        "email": user.email,
        "phone": agent.phone,
        "emirates_id": agent.emirates_id,
        "nationality": agent.nationality,
        "experience": agent.year_of_experience,
        "account_holder_name": agent.account_holder_name,
        "bank_name": agent.bank_name,
        "account_number": agent.account_number,
        "iban": agent.iban,
        "status": "active" if user.is_active else "inactive",
        "commissions": commissions,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }



async def update_agent(session: AsyncSession, agent_id: int, payload: AgentUpdate):

    stmt = (
        select(AgentProfile)
        .where(AgentProfile.id == agent_id)
        .options(selectinload(AgentProfile.user))  # preload user
    )

    result = await session.execute(stmt)
    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    user = agent.user

    data = payload.model_dump(exclude_unset=True)

    agent_fields = [
        "name",
        "phone",
        "emirates_id",
        "nationality",
        "year_of_experience",
        "account_holder_name",
        "bank_name",
        "account_number",
        "iban",
    ]

    for field in agent_fields:
        if field in data:
            setattr(agent, field, data[field])

    if "email" in data:
        user.email = data["email"]

    if "status" in data:
        user.is_active = True if data["status"] == "active" else False

    await session.commit()

    return {
        "message": "Agent updated successfully",
        "id": agent.id
    }



async def delete_agent(
    session: AsyncSession,
    agent_id: int
):

    stmt = select(User).where(
        User.id == agent_id,
        User.role == UserRole.AGENT
    )

    result = await session.execute(stmt)

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Agent not found"
        )

    await session.delete(user)

    await session.commit()

    return {
        "message": "Agent deleted successfully"
    }