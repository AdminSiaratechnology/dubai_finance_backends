from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Table, Column, Text, Boolean, Enum, func
from app.db.base import Base
from datetime import datetime, timezone
from app.sla_template.schemas import SLAStatus
from app.product.models import Product

class SLATemplate(Base):
    __tablename__ = "sla_templates"

    id = Column(Integer, primary_key=True, autoincrement=True,  index=True)

    template_name = Column(String(255), nullable=False)

    telecaller_action_time = Column(Integer, nullable=False, default=0)
    coordinator_verification_time = Column(Integer, nullable=False, default=0)
    submission_time_limit = Column(Integer, nullable=False, default=0)
    escalation_after = Column(Integer, nullable=False, default=0)

    auto_revert_enabled = Column(Boolean, nullable=False, default=True)

    status: Mapped[SLAStatus] = mapped_column(
        Enum(SLAStatus),
        default=SLAStatus.ACTIVE,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    products: Mapped[list["Product"]] = relationship(
    "Product",
    back_populates="sla_template",
    lazy="selectin"
)