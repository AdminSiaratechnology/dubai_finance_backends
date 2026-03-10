from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.email_config.schemas import EmailConfigCreate, EmailConfigOut
from app.email_config.services import fetch_email_config_service, create_or_update_email_config, delete_email_config_service
from app.db.config import SessionDep

router = APIRouter()


@router.get("", response_model=EmailConfigOut)
async def fetch_email_config(session: SessionDep):
    return await fetch_email_config_service(session)


@router.post("", response_model=EmailConfigOut)
async def save_email_config(
    data: EmailConfigCreate,
    session: SessionDep
):
    return await create_or_update_email_config(session, data)   

@router.delete("/{id}")
async def delete_email_config(
    session: SessionDep,
    id: int
):
    return await delete_email_config_service(session, id)