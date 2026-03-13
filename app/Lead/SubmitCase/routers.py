from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.config import SessionDep
from app.account.deps import get_current_user
from app.account.models import User
from app.Lead.SubmitCase.services import submit_complete_case, send_case_otp, get_all_cases,get_case_by_id, get_case_by_lead_id, update_complete_case, get_my_cases
from app.Lead.SubmitCase.schemas import PaginatedCaseOut, CaseDetailOut
router = APIRouter()

@router.post("/case-otp")
async def send_case_otp_router(
    session: SessionDep,
    user: User = Depends(get_current_user),
    email: str = Form(...)
):
    return await send_case_otp(session, email)

@router.post("/submit-complete")
async def submit_complete_case_router(
    session: SessionDep,
    user: User = Depends(get_current_user),
    lead_id: int | None = Form(None),
    customer_name: str = Form(...),
    mobile_number: str = Form(...),
    email: str = Form(...),
    employer_name: str = Form(...),
    emirates_id: str = Form(...),
    monthly_salary: float = Form(...),
    bank_id: int = Form(...),
    product_id: int = Form(...),
    requested_amount: float = Form(...),

    emirates_id_front: UploadFile | None = File(None),
    emirates_id_back: UploadFile | None = File(None),
    passport_copy: UploadFile | None = File(None),
    residence_visa: UploadFile | None = File(None),
    salary_certificate: UploadFile | None = File(None),
    bank_statement_last_3_months: UploadFile | None = File(None),
    bank_statement_last_6_months: UploadFile | None = File(None),
    trade_license: UploadFile | None = File(None),
    liability_letter: UploadFile | None = File(None),
    noc_from_employer: UploadFile | None = File(None),
    security_cheque: UploadFile | None = File(None),
    utility_bill: UploadFile | None = File(None),
    tenancy_contract: UploadFile | None = File(None),
    proof_of_address: UploadFile | None = File(None),
    last_3_month_payslips: UploadFile | None = File(None),
    last_6_month_payslips: UploadFile | None = File(None),
    company_id_card: UploadFile | None = File(None),
    labor_contract: UploadFile | None = File(None),
    employment_letter: UploadFile | None = File(None),
    bank_account_statement: UploadFile | None = File(None),
    credit_report: UploadFile | None = File(None),
    existing_loan_statement: UploadFile | None = File(None),
    property_document: UploadFile | None = File(None),
    vehicle_registration: UploadFile | None = File(None),
    business_plan: UploadFile | None = File(None),
    financial_statement: UploadFile | None = File(None),
    tax_return: UploadFile | None = File(None),
    memorandum_of_association: UploadFile | None = File(None),
    otp: str | None = Form(None),
    status: str | None = Form(None),
):

    return await submit_complete_case(
        session,
        user,
        customer_name,
        mobile_number,
        email,
        employer_name,
        emirates_id,
        monthly_salary,
        bank_id,
        product_id,
        requested_amount,
        emirates_id_front,
        emirates_id_back,
        passport_copy,
        residence_visa,
        salary_certificate,
        bank_statement_last_3_months,
        bank_statement_last_6_months,
        trade_license,
        liability_letter,
        noc_from_employer,
        security_cheque,
        utility_bill,
        tenancy_contract,
        proof_of_address,
        last_3_month_payslips,
        last_6_month_payslips,
        company_id_card,
        labor_contract,
        employment_letter,
        bank_account_statement,
        credit_report,
        existing_loan_statement,
        property_document,
        vehicle_registration,
        business_plan,
        financial_statement,
        tax_return,
        memorandum_of_association,
        otp,
        lead_id, 
        status
    )

@router.get("/", response_model=PaginatedCaseOut)
async def get_cases(
    db: SessionDep,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str | None = None
):  
    return await get_all_cases(db, page, limit, search)

@router.get("/my-cases", response_model=PaginatedCaseOut)
async def get_my_cases_router(
    db: SessionDep,
    user: User = Depends(get_current_user),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    search: str | None = None
):
    return await get_my_cases(db, user, page, limit, search)

@router.get("/{case_id}", response_model=CaseDetailOut)
async def get_case(case_id: int, db: SessionDep):
    case = await get_case_by_id(db, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.get("/{lead_id}/case", response_model=CaseDetailOut)
async def get_case_by_lead(lead_id: int, db: SessionDep):
    case = await get_case_by_lead_id(db, lead_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case


@router.put("/update-case/{case_id}")
async def update_case(
    case_id: int,
    session: SessionDep,
    user: User = Depends(get_current_user),

    customer_name: str | None = Form(None),
    mobile_number: str | None = Form(None),
    email: str | None = Form(None),
    employer_name: str | None = Form(None),
    emirates_id: str | None = Form(None),
    monthly_salary: float | None = Form(None),
    requested_amount: float | None = Form(None),
    status: str | None = Form(None),

    emirates_id_front: UploadFile | None = File(None),
    emirates_id_back: UploadFile | None = File(None),
    passport_copy: UploadFile | None = File(None),
    residence_visa: UploadFile | None = File(None),
    salary_certificate: UploadFile | None = File(None),
    bank_statement_last_3_months: UploadFile | None = File(None),
    bank_statement_last_6_months: UploadFile | None = File(None),
    trade_license: UploadFile | None = File(None),
    liability_letter: UploadFile | None = File(None),
    noc_from_employer: UploadFile | None = File(None),
    security_cheque: UploadFile | None = File(None),
    utility_bill: UploadFile | None = File(None),
    tenancy_contract: UploadFile | None = File(None),
    proof_of_address: UploadFile | None = File(None),
    last_3_month_payslips: UploadFile | None = File(None),
    last_6_month_payslips: UploadFile | None = File(None),
    company_id_card: UploadFile | None = File(None),
    labor_contract: UploadFile | None = File(None),
    employment_letter: UploadFile | None = File(None),
    bank_account_statement: UploadFile | None = File(None),
    credit_report: UploadFile | None = File(None),
    existing_loan_statement: UploadFile | None = File(None),
    property_document: UploadFile | None = File(None),
    vehicle_registration: UploadFile | None = File(None),
    business_plan: UploadFile | None = File(None),
    financial_statement: UploadFile | None = File(None),
    tax_return: UploadFile | None = File(None),
    memorandum_of_association: UploadFile | None = File(None),
):

    return await update_complete_case(
        session,
        case_id,
        user,
        customer_name,
        mobile_number,
        email,
        employer_name,
        emirates_id,
        monthly_salary,
        requested_amount,
        status,

        emirates_id_front,
        emirates_id_back,
        passport_copy,
        residence_visa,
        salary_certificate,
        bank_statement_last_3_months,
        bank_statement_last_6_months,
        trade_license,
        liability_letter,
        noc_from_employer,
        security_cheque,
        utility_bill,
        tenancy_contract,
        proof_of_address,
        last_3_month_payslips,
        last_6_month_payslips,
        company_id_card,
        labor_contract,
        employment_letter,
        bank_account_statement,
        credit_report,
        existing_loan_statement,
        property_document,
        vehicle_registration,
        business_plan,
        financial_statement,
        tax_return,
        memorandum_of_association,
    )

