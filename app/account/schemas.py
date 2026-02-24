from pydantic import BaseModel, EmailStr, Field
from app.account.models import UserRole
from datetime import datetime



class BaseRegister(BaseModel):
    name: str
    email: EmailStr
   



# 🔹 Create Schema (Request Body)
class UserCreate(BaseRegister):
    password: str



class AdminRegister(UserCreate):
    phone: str
    address: str
    # department: str

    




# 🔹 Response Schema
class UserResponse(BaseRegister):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True   # SQLAlchemy ORM support (Pydantic v2)

# -------------------------- Login Schema --------------------



class UserLogin(BaseModel):
  email: EmailStr
  password: str



# ----------------------------- Change Password --------------------------


class PasswordChangeRequest(BaseModel):
  old_password: str = Field(...)
  new_password: str = Field(..., min_length=8)



# ----------------------------------Reset Password ------------------------- 


class PasswordResetEmailRequest(BaseModel):
    email: EmailStr





# ---------------------------------------------------- Profile Schema --------------------------------------

class AdminProfileBase(BaseModel):
    phone: str
    address: str
    # department: str




class AdminProfileResponse(AdminProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True






# ---------------------------------------------------- Profile Schema --------------------------------------