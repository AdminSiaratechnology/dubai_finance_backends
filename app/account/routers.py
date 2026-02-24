from fastapi import APIRouter, HTTPException, status, Depends, Request
from app.account.schemas import (
    AdminRegister,
    UserLogin,
    PasswordChangeRequest,
    PasswordResetEmailRequest,
    UserCreate,
    UserResponse
    
    

) 
from app.db.config import SessionDep
from app.account.services import (
    register_admin_service,
    authenticate_user,
    UserWithProfile,
    get_user_with_profile,
    change_password,
    password_reset_email_send
    
    
)
from app.account.utils import create_tokens, verify_refresh_token
from fastapi.responses import JSONResponse
from app.account.deps import get_current_user
from app.account.models import User


router = APIRouter()


@router.post("/register/admin",status_code=status.HTTP_201_CREATED)
async def register_admin(
    data: AdminRegister,
    db: SessionDep
):
    return await register_admin_service(data, db)




# -------------------------------- Login ---------------------



@router.post("/login")
async def login(session:SessionDep, user_login:UserLogin):
  user = await authenticate_user(session, user_login)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
  
  tokens = await create_tokens(session, user)
#   response = JSONResponse(content={"message": "Login successful"})
  response = JSONResponse(content={
        "message": "Login successful",
        "user": {
            "role": user.role.value   # 👈 important
        }
    })
  response.set_cookie(
    "access_token",
    value=tokens["access_token"],
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=60*60*24*1
  )
  response.set_cookie(
    "refresh_token",
    value=tokens["refresh_token"],
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=60*60*24*7
  )
  return response




# ------------------------------------ Profile -------------------------- 
@router.get("/me", response_model=UserWithProfile, response_model_exclude_none=True)
async def me(
    session: SessionDep,
    current_user: User = Depends(get_current_user),
    
):
    return await get_user_with_profile(session, current_user.id)

# --------------------------------------- Refresh Token --------------------------


@router.post("/refresh")
async def refresh_token(session: SessionDep, request: Request):

    token = request.cookies.get("refresh_token")
    print("REFRESH TOKEN:", token)   # 👈 yaha lagao
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token")
    
    user = await verify_refresh_token(session, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    
    tokens = await create_tokens(session, user)
    response = JSONResponse(content={"message": "Token refreshed successfully"})
    response.set_cookie(
        "access_token",
        value=tokens["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 1
    )
    response.set_cookie(
        "refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7
    )
    return response






# -------------------------------------------- Change Password --------------------------------------



@router.post("/change-password")
async def password_change(session: SessionDep, data: PasswordChangeRequest, user: User= Depends(get_current_user)):
  await change_password(session, user, data)
  return {"msg": "Password changed successfully"}


# -------------------------------------------- Change Password  End--------------------------------------



# -------------------------------------------- Reset Password --------------------------------------


@router.post("/send-password-reset-email")
async def send_password_reset_email(session: SessionDep, data: PasswordResetEmailRequest):
  return await password_reset_email_send(session, data)



# -------------------------------------------- Reset Password End --------------------------------------




