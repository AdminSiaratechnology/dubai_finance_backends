from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey
from datetime import datetime, timezone

from app.db.base import Base


class CaseDocument(Base):
    __tablename__ = "case_documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id", ondelete="CASCADE"))
    emirates_id_front_url: Mapped[str] = mapped_column(String(255), nullable=True)
    emirates_id_back_url: Mapped[str] = mapped_column(String(255), nullable=True)
    passport_copy_url: Mapped[str] = mapped_column(String(255), nullable=True)
    residencevisa_url: Mapped[str] = mapped_column(String(255), nullable=True)
    salary_certificate_url: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_statement_last_3_months_url: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_statement_last_6_months_url: Mapped[str] = mapped_column(String(255), nullable=True)
    trade_license_url: Mapped[str] = mapped_column(String(255), nullable=True)
    liability_letter_url: Mapped[str] = mapped_column(String(255), nullable=True)
    noc_from_employer_url: Mapped[str] = mapped_column(String(255), nullable=True)
    security_cheque_url: Mapped[str] = mapped_column(String(255), nullable=True)
    utility_bill_url: Mapped[str] = mapped_column(String(255), nullable=True)
    tenancy_contract_url: Mapped[str] = mapped_column(String(255), nullable=True)
    proof_of_address_url: Mapped[str] = mapped_column(String(255), nullable=True)
    last_3_month_payslips_url: Mapped[str] = mapped_column(String(255), nullable=True)
    last_6_month_payslips_url: Mapped[str] = mapped_column(String(255), nullable=True)
    company_id_card_url: Mapped[str] = mapped_column(String(255), nullable=True)
    labor_contract_url: Mapped[str] = mapped_column(String(255), nullable=True)
    employment_letter_url: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_account_statement_url: Mapped[str] = mapped_column(String(255), nullable=True)
    credit_report_url: Mapped[str] = mapped_column(String(255), nullable=True)
    existing_loan_statement_url: Mapped[str] = mapped_column(String(255), nullable=True)
    property_document_url: Mapped[str] = mapped_column(String(255), nullable=True)
    vehicle_registration_url: Mapped[str] = mapped_column(String(255), nullable=True)
    business_plan_url: Mapped[str] = mapped_column(String(255), nullable=True)
    financial_statement_url: Mapped[str] = mapped_column(String(255), nullable=True)
    tax_return_url: Mapped[str] = mapped_column(String(255), nullable=True)
    memorandum_of_association_url: Mapped[str] = mapped_column(String(255), nullable=True)
    
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
   

    # relationship
    case = relationship("Case", back_populates="documents")