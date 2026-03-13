
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Text, Numeric
from app.db.base import Base
from app.product.schemas import CustomerSegment,ProductStatus
from sqlalchemy.orm import relationship,Mapped


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.loantype.models import Bank, LoanType
    from app.sla_template.models import SLATemplate
    from app.commission.models import Commission
    
    

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String(255), nullable=False)

    customer_segment = Column(
        Enum(CustomerSegment, name="customer_segment_enum"),
        nullable=False
    )

    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="CASCADE"), nullable=False)
    loan_type_id = Column(Integer, ForeignKey("loan_types.id"), nullable=False)
    sla_template_id = Column(Integer, ForeignKey("sla_templates.id"))

    min_loan_amount = Column(Numeric(12, 2), nullable=False)
    max_loan_amount = Column(Numeric(12, 2), nullable=False)

    min_tenure = Column(Integer, nullable=False)
    max_tenure = Column(Integer, nullable=False)

    processing_fee = Column(Numeric(10, 2), default=0)
    priority_score = Column(Integer, default=50)

    internal_notes = Column(Text, nullable=True)

    status = Column(
        Enum(ProductStatus, name="product_status_enum"),
        default=ProductStatus.active
    )

    bank: Mapped["Bank"] = relationship("Bank", back_populates="products")
    loan_type: Mapped["LoanType"] = relationship(
        "LoanType",
        back_populates="products"
    )
    sla_template: Mapped["SLATemplate"] = relationship(
        "SLATemplate",
        back_populates="products"
    )
    # commissions: Mapped[list["Commission"]] = relationship(back_populates="products",  lazy="selectin")
    commissions: Mapped[list["Commission"]] = relationship(
        "Commission",
        back_populates="product",
        lazy="selectin"
    )
    # lLeads
    leads = relationship(
        "Lead",
        back_populates="product"
    )
    case = relationship(
        "Case",
        back_populates="product"
    )