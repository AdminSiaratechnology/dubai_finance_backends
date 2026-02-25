from pydantic import BaseModel, EmailStr, Field, field_validator
from app.account.models import UserRole
from datetime import datetime



class BaseRegister(BaseModel):
    
    email: EmailStr
    
   



# 🔹 Create Schema (Request Body)
class UserCreate(BaseRegister):
    password: str



class AdminRegister(UserCreate):
    name : str
    phone: str
    address: str
    # department: str

    




# 🔹 Response Schema
class UserResponse(BaseRegister):
    role: str
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



class PasswordResetRequest(BaseModel):
  token: str 
  new_password: str = Field(..., min_length=8)
  @field_validator("new_password")
  @classmethod
  def validate_new_password_strength(cls, value: str) -> str:
    if value.lower() == value or value.upper() == value:
      raise ValueError("Password must contain both uppercase and lowercase letters")
    if not any(char.isdigit() for char in value):
      raise ValueError("Password must contain at least one digit")
    return value



# ---------------------------------------------------- Profile Schema --------------------------------------

class AdminProfileBase(BaseModel):
    phone: str
    address: str
    # department: str




class AdminProfileResponse(AdminProfileBase):
    id: int
    user_id: int
    name : str

    class Config:
        from_attributes = True





# ---------------------------------------------------- Profile Schema --------------------------------------