from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from app.email_config.models import EmailConfiguration


# Get email config (returns None if not found)
async def get_email_config(session: AsyncSession):
    result = await session.execute(select(EmailConfiguration))
    return result.scalars().first()


# Fetch config with 404 validation
async def fetch_email_config_service(session: AsyncSession):
    config = await get_email_config(session)

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )

    return config


# Create or Update config
async def create_or_update_email_config(session: AsyncSession, data):

    config = await get_email_config(session)

    if config:
        config.smtp_user = data.smtp_user
        config.smtp_password = data.smtp_password
    else:
        config = EmailConfiguration(
            smtp_user=data.smtp_user,
            smtp_password=data.smtp_password
        )
        session.add(config)

    await session.commit()
    await session.refresh(config)

    return config


# Delete config
async def delete_email_config_service(session: AsyncSession, id: int):

    result = await session.execute(
        select(EmailConfiguration).where(EmailConfiguration.id == id)
    )
    config = result.scalars().first()

    if not config:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email configuration not found"
        )

    await session.delete(config)
    await session.commit()

    return {"message": "Email configuration deleted successfully"}