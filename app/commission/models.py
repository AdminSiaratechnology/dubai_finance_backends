
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Table, Column, Text, Boolean, Enum
from app.db.base import Base
from datetime import datetime, timezone

from app.commission.schemas import LoanStatus 


loantype_bank_table = Table(
    "bank_loan_types",
    Base.metadata,
    Column("bank_id", Integer, ForeignKey("banks.id", ondelete="CASCADE"), primary_key=True),
    Column("loan_type_id", Integer, ForeignKey("loan_types.id", ondelete="CASCADE"), primary_key=True)
)



class Bank(Base):
  __tablename__ = "banks"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  short_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  default_tat_days: Mapped[int] = mapped_column(default=0)
  description: Mapped[str] = mapped_column(Text, nullable=True)
  image_url: Mapped[str] = mapped_column(String(255), nullable=True)
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))

  loan_types: Mapped[list["LoanType"]] = relationship("LoanType", secondary=loantype_bank_table, back_populates="banks")
  



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





# class CartItem(Base):
#   __tablename__ = "cart_items"

#   id: Mapped[int] = mapped_column(primary_key=True, index=True)
#   user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#   product_id: Mapped[int | None] = mapped_column(ForeignKey("products.id", ondelete="SET NULL"), nullable=True)
#   quantity: Mapped[int] = mapped_column(default=1)
#   price: Mapped[float] = mapped_column(Float, nullable=False)

#   user: Mapped["User"] = relationship("User", back_populates="cart_items")
#   product: Mapped["Product"] = relationship("Product", back_populates="cart_items")