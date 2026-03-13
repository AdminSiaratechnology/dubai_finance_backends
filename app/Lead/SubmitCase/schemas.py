from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.loantype.schemas import BankLite
from app.Lead.SubmitLead.schemas import ProductLite

class CaseDocumentOut(BaseModel):
    emirates_id_front_url: Optional[str]
    emirates_id_back_url: Optional[str]
    passport_copy_url: Optional[str]
    residencevisa_url: Optional[str]
    salary_certificate_url: Optional[str]
    bank_statement_last_3_months_url: Optional[str]
    bank_statement_last_6_months_url: Optional[str]
    trade_license_url: Optional[str]
    liability_letter_url: Optional[str]
    noc_from_employer_url: Optional[str]
    security_cheque_url: Optional[str]
    utility_bill_url: Optional[str]
    tenancy_contract_url: Optional[str]
    proof_of_address_url: Optional[str]
    last_3_month_payslips_url: Optional[str]
    last_6_month_payslips_url: Optional[str]
    company_id_card_url: Optional[str]
    labor_contract_url: Optional[str]
    employment_letter_url: Optional[str]
    bank_account_statement_url: Optional[str]
    credit_report_url: Optional[str]
    existing_loan_statement_url: Optional[str]
    property_document_url: Optional[str]
    vehicle_registration_url: Optional[str]
    business_plan_url: Optional[str]
    financial_statement_url: Optional[str]
    tax_return_url: Optional[str]
    memorandum_of_association_url: Optional[str]

    class Config:
        from_attributes = True


class CaseOut(BaseModel):
    id: int
    agent_id: int
    customer_name: str
    mobile_number: str
    email: Optional[str]
    product: Optional[ProductLite]
    bank: Optional[BankLite]
    requested_amount: float

    salary: Optional[float]
    company_name: Optional[str]

    emirates_id: Optional[str]
    passport_no: Optional[str]

    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class CaseDetailOut(CaseOut):
    documents: Optional[List[CaseDocumentOut]]


class PaginatedCaseOut(BaseModel):
    total: int
    page: int
    limit: int
    items: List[CaseDetailOut]