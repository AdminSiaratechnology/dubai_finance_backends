from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Table, Column, Text, Boolean, Enum
from datetime import datetime, timezone
from app.loantype.schemas import LoanStatus
from app.loantype.models import loantype_bank_table
from typing import TYPE_CHECKING
if TYPE_CHECKING:
 
  from app.loantype.models import LoanType
  from app.category.models import BankCategory
  from app.product.models import Product
  from app.commission.models import Commission
class Bank(Base):
  __tablename__ = "banks"

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(255), nullable=False)
  short_code: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
  default_tat_days: Mapped[int] = mapped_column(default=0)
  description: Mapped[str] = mapped_column(Text, nullable=True)
  status: Mapped[LoanStatus] = mapped_column(
        Enum(LoanStatus, name="bank_status_enum"),
        nullable=True,                # initially True for safe migration
        default=LoanStatus.active,    # SQLAlchemy default
        server_default="active"       # PostgreSQL default
    )
  logo_url: Mapped[str] = mapped_column(String(255), nullable=True)
  category_id: Mapped[int] = mapped_column(Integer, ForeignKey("bank_categories.id", ondelete="SET NULL"), nullable=True)
#   products = relationship("Product", back_populates="bank", cascade="all, delete")
 
  created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
  updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),onupdate=lambda: datetime.now(timezone.utc))


  category: Mapped["BankCategory"] = relationship(
        "BankCategory",
        back_populates="banks",
        lazy="selectin"
    )
  loan_types: Mapped[list["LoanType"]] = relationship("LoanType", secondary=loantype_bank_table, back_populates="banks", lazy="selectin")

  products: Mapped[list["Product"]] = relationship(
    "Product",
    back_populates="bank",
    cascade="all, delete-orphan",
    lazy="selectin"
)
  commissions: Mapped[list["Commission"]] = relationship(back_populates="bank",  lazy="selectin")
  leads = relationship("Lead", back_populates="bank")
  case = relationship("Case", back_populates="bank")