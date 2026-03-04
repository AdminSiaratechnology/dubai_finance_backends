
from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Table, Column, Text, Boolean, Enum
from app.loantype.schemas import LoanStatus 
from datetime import datetime, timezone
from app.Bank.models import Bank

class BankCategory(Base):
    __tablename__ = "bank_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus),
        nullable=True,                # initially True for safe migration
        default=LoanStatus.active,    # SQLAlchemy default
        server_default="active"       # PostgreSQL default
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

    # One-to-Many: A category has multiple banks
    banks: Mapped[list["Bank"]] = relationship(
        "Bank",
        back_populates="category"
    )

    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable= True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc), nullable=True)

