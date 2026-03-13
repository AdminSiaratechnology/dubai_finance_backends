from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from typing import Optional
from app.db.base import Base

class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    lead_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("leads.id"), nullable=True
    )

    agent_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    telecaller_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    customer_name: Mapped[str] = mapped_column(String(150))
    mobile_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150))

    # product_type: Mapped[int] = mapped_column(ForeignKey("products.id"),nullable=True)
    requested_amount: Mapped[float] = mapped_column(Float)

    salary: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    product_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True
    )

    bank_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("banks.id", ondelete="SET NULL"),
        nullable=True
    )
    emirates_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    passport_no: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    status: Mapped[str] = mapped_column(String(50), default="draft")

    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime, default=lambda: datetime.now(timezone.utc)
    # )
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
)

    # relationships
    # lead = relationship("Lead", back_populates="case")
    bank = relationship(
        "Bank",
        back_populates="case",
        lazy="selectin"
    )
    product = relationship(
        "Product",
        back_populates="case",
        lazy="selectin"
    )
    documents = relationship(
        "CaseDocument",
        back_populates="case",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    lead = relationship(
        "Lead",
        back_populates="case",
        lazy="selectin"
    )