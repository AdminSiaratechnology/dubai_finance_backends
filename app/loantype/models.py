
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Table, Column, Text, Boolean, Enum
from app.db.base import Base
from datetime import datetime, timezone
from app.loantype.schemas import LoanStatus 
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.product.models import Product
    from app.Bank.models import Bank

loantype_bank_table = Table(
    "bank_loan_types",
    Base.metadata,
    Column("bank_id", Integer, ForeignKey("banks.id", ondelete="CASCADE"), primary_key=True),
    Column("loan_type_id", Integer, ForeignKey("loan_types.id", ondelete="CASCADE"), primary_key=True)
)


class LoanType(Base):
  __tablename__ = "loan_types"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

  status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus, name="loan_status_enum"),
        nullable=True,                # initially True for safe migration
        default=LoanStatus.active,    # SQLAlchemy default
        server_default="active"       # PostgreSQL default
    )
  description: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

  banks: Mapped[list["Bank"]] = relationship("Bank", secondary=loantype_bank_table, back_populates="loan_types")
  products: Mapped[list["Product"]] = relationship(
    "Product",
    back_populates="loan_type",
    lazy="selectin"
)

  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable= True)
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc), nullable=True)


