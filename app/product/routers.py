from fastapi import APIRouter, Depends,HTTPException,status,Query 
from typing import List, Annotated, Optional
from app.account.deps import require_admin,User
from app.db.config import SessionDep
from app.product.schemas import ProductOut, ProductCreate,PaginatedProductOut, ProductStatus
from app.product.services import product_create, get_all_products, get_product_by_id, update_product, delete_product




router = APIRouter()

@router.post("/", response_model=ProductOut)
async def create_product(
    session: SessionDep,
    product: ProductCreate,
    admin_user: User = Depends(require_admin)

):
    return await product_create(session, product)


# 🔹 Get All Banks
@router.get("/", response_model=PaginatedProductOut)
async def get_all_products_api(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),

    
    # status: Optional[LoanStatus] = Query(LoanStatus.active, description="Filter by loan status"),
    status: Optional[ProductStatus] = Query(
        None,   # 👈 changed from LoanStatus.active
        description="Filter by product status"
    ),
    admin_user: User = Depends(require_admin)
):
    return await get_all_products(session, page, limit, search, status)



@router.get("/{product_id}",response_model=ProductOut)
async def get_product(
    product_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    product = await get_product_by_id(session, product_id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product




# ✅ Update Product

@router.put("/{product_id}", response_model=ProductOut)
async def product_update(
    product_id: int,
    product_data: ProductCreate,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await update_product(
        session,
        product_id,
        product_data
    )



# Delete Product
@router.delete("/{product_id}")
async def product_delete(
    product_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)   
):
    result = await delete_product(session, product_id)
    return result
    

