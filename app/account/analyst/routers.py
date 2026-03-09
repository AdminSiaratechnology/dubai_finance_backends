


from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.db.config import SessionDep
from app.account.models import User
from app.account.deps import require_admin
from typing import Optional

from app.account.analyst.schemas import CoordinatorCreate, CoordinatorOut, PaginatedCoordinator, CoordinatorStatus,CoordinatorUpdate
from app.account.analyst.services import create_coordinator,allcoordinator, get_coordinator_by_id, update_coordinator,delete_coordinator

router = APIRouter()

@router.post("/",response_model=CoordinatorOut,status_code=status.HTTP_201_CREATED)
async def register_coordinator(
    session: SessionDep,
    coordinator: CoordinatorCreate,
    admin_user: User = Depends(require_admin)
    
):
    return await create_coordinator(session, coordinator)


   

# 🔹 Get All Banks
@router.get("/", response_model=PaginatedCoordinator)
async def get_all_coordinator(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(5, ge=1),
    search: Optional[str] = Query(None),
    status: Optional[CoordinatorStatus] = Query(CoordinatorStatus.active, description="Filter by loan status"),
    admin_user: User = Depends(require_admin)
):
    return await allcoordinator(session, page, limit, search, status)

@router.get("/{coordinator_id}", response_model=CoordinatorOut)
async def get_coordinator(
    coordinator_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await get_coordinator_by_id(session, coordinator_id)



@router.put("/{coordinator_id}", response_model=CoordinatorOut)
async def update_coordinator_api(
    coordinator_id: int,
    data: CoordinatorUpdate,
    session: SessionDep,
    # admin_user: User = Depends(require_admin)
):
    return await update_coordinator(session, coordinator_id, data)



@router.delete("/{coordinator_id}")
async def delete_coordinator_api(
    coordinator_id: int,
    session: SessionDep,
    admin_user: User = Depends(require_admin)
):
    return await delete_coordinator(session, coordinator_id)