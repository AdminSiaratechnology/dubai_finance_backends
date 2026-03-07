from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Enum, Index
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.sql import func
import enum
from datetime import datetime, date, timezone
from app.commission.association import agent_commission_table
from app.db.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.Bank.models import Bank
    from app.product.models import Product
    from app.account.models import AgentProfile
    

class CommissionTypeEnum(str, enum.Enum):
    percentage = "percentage"
    flat = "flat"

class CommissionStatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"    


class Commission(Base):
    __tablename__ = "commissions"

    # Composite Indexes
    __table_args__ = (
        Index("idx_commission_bank", "bank_id"),
        Index("idx_commission_product", "product_id"),
        Index("idx_commission_status", "status"),
        Index("idx_commission_effective_date", "effective_from_date"),
        Index("idx_commission_bank_product", "bank_id", "product_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    bank_id: Mapped[int] = mapped_column(ForeignKey("banks.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    commission_type: Mapped[CommissionTypeEnum] = mapped_column(Enum(CommissionTypeEnum))
    commission_value: Mapped[float] = mapped_column(Float)

    agent_share: Mapped[float] = mapped_column(Float, default=0)
    telecaller_share: Mapped[float] = mapped_column(Float, default=0)
    coordinator_share: Mapped[float] = mapped_column(Float, default=0)

    effective_from_date: Mapped[date] = mapped_column(Date)

    status: Mapped[CommissionStatusEnum] = mapped_column(
        Enum(CommissionStatusEnum),
        default=CommissionStatusEnum.active
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    bank: Mapped["Bank"] = relationship(
        back_populates="commissions",
        lazy="selectin"
    )

    product: Mapped["Product"] = relationship(
        back_populates="commissions",
        lazy="selectin"
    )

    agents: Mapped[list["AgentProfile"]] = relationship(
        "AgentProfile",
        secondary=agent_commission_table,
        back_populates="commissions",
        lazy="selectin"
    )