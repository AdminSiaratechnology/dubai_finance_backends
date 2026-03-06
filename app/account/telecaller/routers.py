from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.db.config import SessionDep
from app.account.models import User
from app.account.deps import require_admin
from typing import Optional

from app.account.telecaller.schemas import TelecallerCreate, TelecallerOut, PaginatedTelecaller, TelecallerStatus,TelecallerUpdate
from app.account.telecaller.services import create_telecaller,alltelecaller, get_telecaller_by_id, update_telecaller,delete_telecaller

router = APIRouter()

@router.post("/",response_model=TelecallerOut,status_code=status.HTTP_201_CREATED)
async def register_telecaller(
    session: SessionDep,
    telecaller: TelecallerCreate,
    admin_user: User = Depends(require_admin)
    
):
    return await create_telecaller(session, telecaller)


   

# 🔹 Get All Banks
@router.get("/", response_model=PaginatedTelecaller)
async def get_all_telecaller(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),
    status: Optional[TelecallerStatus] = Query(TelecallerStatus.active, description="Filter by loan status"),
    admin_user: User = Depends(require_admin)
):
    return await alltelecaller(session, page, limit, search, status)

@router.get("/{telecaller_id}", response_model=TelecallerOut)
async def get_telecaller(
    telecaller_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_telecaller_by_id(session, telecaller_id)



@router.put("/{telecaller_id}", response_model=TelecallerOut)
async def update_telecaller_api(
    telecaller_id: int,
    data: TelecallerUpdate,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await update_telecaller(session, telecaller_id, data)



@router.delete("/{telecaller_id}")
async def delete_coordinator_api(
    telecaller_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await delete_telecaller(session, telecaller_id)
    