from fastapi import APIRouter, Depends,HTTPException,status,Query 
from typing import List, Annotated, Optional
from app.account.deps import require_admin,User
from app.db.config import SessionDep
from app.product.schemas import ProductOut, ProductCreate
from app.product.services import product_create




router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create_product(
    session: SessionDep,
    product: ProductCreate,
    admin_user: User = Depends(require_admin)

):
    return await product_create(session, product)
