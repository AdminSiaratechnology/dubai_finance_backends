from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from datetime import datetime, timezone
from app.db.base import Base
from typing import Optional



class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # agent who created the lead
    agent_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    # telecaller assigned via round robin
    telecaller_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    customer_name: Mapped[str] = mapped_column(String(150))
    mobile_number: Mapped[str] = mapped_column(String(20))
    email: Mapped[str] = mapped_column(String(150))

    product_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("products.id", ondelete="SET NULL"),
        nullable=True
    )

    bank_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("banks.id", ondelete="SET NULL"),
        nullable=True
    )

    requested_amount: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    # ---------------- RELATIONSHIPS ----------------

    # one lead → one case
    case = relationship(
        "Case",
        back_populates="lead",
        uselist=False,
        lazy="selectin"
    )

    # lead → product
    product = relationship(
        "Product",
        back_populates="leads",
        lazy="selectin"
    )

    # lead → agent user
    agent = relationship(
        "User",
        foreign_keys=[agent_id],
        lazy="selectin"
    )

    # lead → assigned telecaller
    telecaller = relationship(
        "User",
        foreign_keys=[telecaller_id],
        lazy="selectin"
    )

    bank = relationship(
        "Bank",
        back_populates="leads",
        lazy="selectin"
    )

class EmailOTP(Base):
    __tablename__ = "email_otps"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    otp: Mapped[str] = mapped_column(String, nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)