from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base import Base

agent_commission_table = Table(
    "agent_commissions",
    Base.metadata,
    Column("agent_id", Integer, ForeignKey("agent_profiles.id"), primary_key=True, index=True),
    Column("commission_id", Integer, ForeignKey("commissions.id"), primary_key=True, index=True),
)