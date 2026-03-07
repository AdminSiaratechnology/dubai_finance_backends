from fastapi import APIRouter, Depends, HTTPException, status,Query
from app.db.config import SessionDep
from app.account.models import User
from app.account.deps import require_admin
from typing import Optional
from app.account.agent.schemas import AgentCreate, AgentOut, AgentStatus,AgentUpdate, PaginatedAgentOut #PaginatedAgent
from app.account.agent.services import create_agent, get_all_agents, get_agent_by_id, update_agent, delete_agent


router = APIRouter()

@router.post("/", response_model=AgentOut, status_code=status.HTTP_201_CREATED)
async def register_agent(
    session: SessionDep,
    agent: AgentCreate,
    # admin_user: User = Depends(require_admin)
):
    return await create_agent(session, agent)


@router.get("/", response_model=PaginatedAgentOut)
async def all_agents(
    session: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str | None = None,
    status: AgentStatus | None = None
):
    return await get_all_agents(session, page, limit, search, status)

@router.get("/{agent_id}")
async def get_agent(
    session: SessionDep,
    agent_id: int
):
    return await get_agent_by_id(session, agent_id)



@router.put("/{agent_id}")
async def agent_update(
    session: SessionDep,
    agent_id: int,
    payload: AgentUpdate,
    
):
    return await update_agent(session, agent_id, payload)


@router.delete("/{agent_id}")
async def agent_delete(
    session: SessionDep,
    agent_id: int,
    
):
    return await delete_agent(session, agent_id)