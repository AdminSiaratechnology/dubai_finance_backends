from app.account.models import User, UserRole, AdminProfile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app.account.utils import hash_password, verify_password, get_user_by_email, create_password_reset_token,verify_email_token_and_get_user_id,send_email
from app.account.schemas import AdminRegister, AgentProfileResponse,UserLogin,UserResponse,AdminProfileResponse,TelecallerProfileResponse,CoordinatorProfileResponse,PasswordChangeRequest,PasswordResetEmailRequest,PasswordResetRequest,UpdateAdminProfile
from sqlalchemy.orm import selectinload
from typing import Optional
from app.account.agent.schemas import AgentOut



async def check_email_exists(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def register_admin_service(data: AdminRegister, db: AsyncSession):

    if await check_email_exists(data.email, db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    try:
        user = User(
            
            email=data.email,
            password_hash=hash_password(data.password),
            role=UserRole.ADMIN
        )
        db.add(user)
        await db.flush()

        profile = AdminProfile(
            user_id=user.id,
            name = data.name,
            phone=data.phone,
            address=data.address,
        )
        db.add(profile)
        await db.commit() 

        return {"message": "Admin registered successfully"}

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))




# -------------------------------- Login ----------------------- 


async def authenticate_user(session: AsyncSession, user_login: UserLogin):
  stmt = select(User).where(User.email == user_login.email)
  result = await session.scalars(stmt)
  user = result.first()

  if not user or not verify_password(user_login.password, user.password_hash):
    return None
  
  return user




# ----------------------------------------- Change Password ------------------------


async def change_password(session: AsyncSession, user: User, data: PasswordChangeRequest):
  if not verify_password(data.old_password, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")
  user.password_hash = hash_password(data.new_password)
  session.add(user)
  await session.commit()


# ----------------------------------------- Change Password ------------------------



# ------------------------------------------- Password Reset Email --------------------------


# async def password_reset_email_send(session: AsyncSession, data: PasswordResetEmailRequest):
#   user = await get_user_by_email(session, data.email)
#   if not user:
#       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#   token = create_password_reset_token(user.id)
  
#   link = f"http://localhost:8000/account/password-reset?token={token}"
#   print(f"Reset your password: {link}")
#   return {"msg": "Password reset link sent"}

async def password_reset_email_send(session: AsyncSession, data: PasswordResetEmailRequest):
    user = await get_user_by_email(session, data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    token = create_password_reset_token(user.id)

    link = f"https://l26sd4rg-3000.inc1.devtunnels.ms/reset-password?token={token}"

    await send_email(
        session=session,
        to_email=user.email,
        subject="Password Reset Request",
        body=f"""
Hello,

Click the link below to reset your password:

{link}

If you did not request this, please ignore this email.
"""
    )

    return {"msg": "Password reset link sent to your email"}


async def verify_password_reset_token(session: AsyncSession, data: PasswordResetRequest):
  user_id = verify_email_token_and_get_user_id(data.token, "password_reset")
  if not user_id:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")
  
  stmt = select(User).where(User.id == user_id)
  result = await session.scalars(stmt)
  user = result.first()

  if not user: 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
  
  user.password_hash = hash_password(data.new_password)
  session.add(user)
  await session.commit()
  return {"msg": "Password reset successful"}

# ------------------------------------------- Password Reset Email End --------------------------





class UserWithProfile(UserResponse):
    admin_profile: Optional[AdminProfileResponse] = None
    agent_profile: Optional[AgentProfileResponse] = None
    telecaller_profile: Optional[TelecallerProfileResponse] = None
    coordinator_profile: Optional[CoordinatorProfileResponse] = None

async def get_user_with_profile(
    session: AsyncSession,
    user_id: int
):
    stmt = (
        select(User)
        .options(
            selectinload(User.admin_profile),
            selectinload(User.agent_profile),
            selectinload(User.telecaller_profile),
            selectinload(User.coordinator_profile),
        )
        .where(User.id == user_id)
    )

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

async def update_user_profile(session: AsyncSession, user_id: int, data: UpdateAdminProfile):

    stmt = select(AdminProfile).where(AdminProfile.user_id == user_id)
    result = await session.execute(stmt)
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile.name = data.name
    profile.phone = data.phone
    profile.address = data.address

    await session.commit()
    await session.refresh(profile)

    return profile