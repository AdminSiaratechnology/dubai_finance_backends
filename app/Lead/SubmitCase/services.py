from sqlalchemy.ext.asyncio import AsyncSession
from app.Lead.SubmitCase.models import Case
from app.Lead.LeadDocuments.models import CaseDocument
from app.loantype.utils import save_upload_file
import random
from datetime import datetime, timedelta
from app.account.utils import send_email
from fastapi import HTTPException
from sqlalchemy import select, delete
from app.account.models import User
from app.Lead.SubmitLead.models import EmailOTP
from sqlalchemy import select, func,or_
from app.Lead.SubmitLead.models import Lead

async def send_case_otp(db:AsyncSession, email: str):
    otp = str(random.randint(100000, 999999))
    
    await db.execute(
        delete(EmailOTP).where(EmailOTP.email == email)
    )

    otp_record = EmailOTP(
        email=email,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=5)
    )

    db.add(otp_record)
    await db.commit()

    await send_email(
        session=db,
        to_email=email,
        subject="Case Verification OTP",
        body=f"Your OTP is {otp}. It will expire in 5 minutes."
    )

    return {"message": "OTP sent successfully"}

async def submit_complete_case(
    db: AsyncSession,
    user: User,
    customer_name: str,
    mobile_number: str,
    email: str,
    employer_name: str,
    emirates_id: str,
    monthly_salary: float,
    bank_id: int,
    product_id: int,
    requested_amount: float,
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
    otp: str | None = None,
    lead_id: int | None = None,
    status: str | None = None,
):
    try:

        if user.role == "agent":

            if not otp:
                raise HTTPException(status_code=400, detail="OTP required")

            result = await db.execute(
                select(EmailOTP).where(EmailOTP.email == email)
            )

            otp_record = result.scalars().first()

            if not otp_record:
                raise HTTPException(status_code=400, detail="OTP not found")

            if otp_record.otp != otp:
                raise HTTPException(status_code=400, detail="Invalid OTP")

            if otp_record.expires_at < datetime.utcnow():
                raise HTTPException(status_code=400, detail="OTP expired")

            await db.execute(
                delete(EmailOTP).where(EmailOTP.email == email)
            )

        if lead_id:
            lead_result = await db.execute(
                select(Lead).where(Lead.id == lead_id)
            )

            lead = lead_result.scalar_one_or_none()

            if not lead:
                raise HTTPException(status_code=404, detail="Lead not found")

        agent_id = None
        telecaller_id = None

        if user.role == "agent":
            agent_id = user.id

        else:
            telecaller_id = user.id

            if not lead_id:
                raise HTTPException(status_code=400, detail="Lead ID required")

            lead_result = await db.execute(
                select(Lead).where(Lead.id == lead_id)
            )

            lead = lead_result.scalar_one_or_none()

            if not lead:
                raise HTTPException(status_code=404, detail="Lead not found")

            agent_id = lead.agent_id

        case = Case(
            lead_id=lead_id,
            agent_id=agent_id,
            telecaller_id=telecaller_id,
            customer_name=customer_name,
            mobile_number=mobile_number,
            email=email,
            salary=monthly_salary,
            requested_amount=requested_amount,
            status=status,
            company_name=employer_name,
            emirates_id=emirates_id,
            bank_id= bank_id,
            product_id = product_id
        )

        db.add(case)
        await db.flush()

        case_id = case.id

        emirates_front_url = await save_upload_file(emirates_id_front, f"cases/{case_id}")
        emirates_back_url = await save_upload_file(emirates_id_back, f"cases/{case_id}")
        passport_copy_url = await save_upload_file(passport_copy, f"cases/{case_id}")
        residencevisa_url = await save_upload_file(residence_visa, f"cases/{case_id}")
        salary_certificate_url = await save_upload_file(salary_certificate, f"cases/{case_id}")
        bank_statement_last_3_months_url = await save_upload_file(bank_statement_last_3_months, f"cases/{case_id}")
        bank_statement_last_6_months_url = await save_upload_file(bank_statement_last_6_months, f"cases/{case_id}")
        trade_license_url = await save_upload_file(trade_license, f"cases/{case_id}")
        liability_letter_url = await save_upload_file(liability_letter, f"cases/{case_id}")
        noc_from_employer_url = await save_upload_file(noc_from_employer, f"cases/{case_id}")
        security_cheque_url = await save_upload_file(security_cheque, f"cases/{case_id}")
        utility_bill_url = await save_upload_file(utility_bill, f"cases/{case_id}")
        tenancy_contract_url = await save_upload_file(tenancy_contract, f"cases/{case_id}")
        proof_of_address_url = await save_upload_file(proof_of_address, f"cases/{case_id}")
        last_3_month_payslips_url = await save_upload_file(last_3_month_payslips, f"cases/{case_id}")
        last_6_month_payslips_url = await save_upload_file(last_6_month_payslips, f"cases/{case_id}")
        company_id_card_url = await save_upload_file(company_id_card, f"cases/{case_id}")
        labor_contract_url = await save_upload_file(labor_contract, f"cases/{case_id}")
        employment_letter_url = await save_upload_file(employment_letter, f"cases/{case_id}")
        bank_account_statement_url = await save_upload_file(bank_account_statement, f"cases/{case_id}")
        credit_report_url = await save_upload_file(credit_report, f"cases/{case_id}")
        existing_loan_statement_url = await save_upload_file(existing_loan_statement, f"cases/{case_id}")
        property_document_url = await save_upload_file(property_document, f"cases/{case_id}")
        vehicle_registration_url = await save_upload_file(vehicle_registration, f"cases/{case_id}")
        business_plan_url = await save_upload_file(business_plan, f"cases/{case_id}")
        financial_statement_url = await save_upload_file(financial_statement, f"cases/{case_id}")
        tax_return_url = await save_upload_file(tax_return, f"cases/{case_id}")
        memorandum_of_association_url = await save_upload_file(memorandum_of_association, f"cases/{case_id}")
        documents = CaseDocument(
            case_id=case_id,
            emirates_id_front_url=emirates_front_url,
            emirates_id_back_url=emirates_back_url,
            passport_copy_url=passport_copy_url,
            residencevisa_url=residencevisa_url,
            salary_certificate_url=salary_certificate_url,
            bank_statement_last_3_months_url=bank_statement_last_3_months_url,
            bank_statement_last_6_months_url=bank_statement_last_6_months_url,
            trade_license_url=trade_license_url,
            liability_letter_url=liability_letter_url,
            noc_from_employer_url=noc_from_employer_url,
            security_cheque_url=security_cheque_url,
            utility_bill_url=utility_bill_url,
            tenancy_contract_url=tenancy_contract_url,
            proof_of_address_url=proof_of_address_url,
            last_3_month_payslips_url=last_3_month_payslips_url,
            last_6_month_payslips_url=last_6_month_payslips_url,
            company_id_card_url=company_id_card_url,
            labor_contract_url=labor_contract_url,
            employment_letter_url=employment_letter_url,
            bank_account_statement_url=bank_account_statement_url,
            credit_report_url=credit_report_url,
            existing_loan_statement_url=existing_loan_statement_url,
            property_document_url=property_document_url,
            vehicle_registration_url=vehicle_registration_url,
            business_plan_url=business_plan_url,
            financial_statement_url=financial_statement_url,
            tax_return_url=tax_return_url,
            memorandum_of_association_url=memorandum_of_association_url
        )

        db.add(documents)

        await db.commit()

        return {
            "message": "Case submitted successfully",
            "case_id": case_id
        }

    except Exception as e:
        await db.rollback()
        raise e


async def get_all_cases(db, page: int = 1, limit: int = 10, search: str | None = None):

    offset = (page - 1) * limit

    query = select(Case)

    if search:
        query = query.where(
            or_(
                Case.customer_name.ilike(f"%{search}%"),
                Case.mobile_number.ilike(f"%{search}%"),
                Case.email.ilike(f"%{search}%"),
                Case.passport_no.ilike(f"%{search}%"),
                Case.emirates_id.ilike(f"%{search}%")
            )
        )

    # total count
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar()

    # pagination
    result = await db.execute(
        query.offset(offset).limit(limit)
    )

    cases = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": cases
    }

async def get_case_by_id(db, case_id: int):

    result = await db.execute(
        select(Case).where(Case.id == case_id)
    )

    case = result.scalar_one_or_none()

    return case

async def get_case_by_lead_id(db, lead_id: int):
    result = await db.execute(
        select(Case).where(Case.lead_id == lead_id)
    )

    case = result.scalar_one_or_none()

    return case


async def update_complete_case(
    db: AsyncSession,
    case_id: int,
    user: User,
    customer_name: str | None = None,
    mobile_number: str | None = None,
    email: str | None = None,
    employer_name: str | None = None,
    emirates_id: str | None = None,
    monthly_salary: float | None = None,
    requested_amount: float | None = None,
    status: str | None = None,

    emirates_id_front=None,
    emirates_id_back=None,
    passport_copy=None,
    residence_visa=None,
    salary_certificate=None,
    bank_statement_last_3_months=None,
    bank_statement_last_6_months=None,
    trade_license=None,
    liability_letter=None,
    noc_from_employer=None,
    security_cheque=None,
    utility_bill=None,
    tenancy_contract=None,
    proof_of_address=None,
    last_3_month_payslips=None,
    last_6_month_payslips=None,
    company_id_card=None,
    labor_contract=None,
    employment_letter=None,
    bank_account_statement=None,
    credit_report=None,
    existing_loan_statement=None,
    property_document=None,
    vehicle_registration=None,
    business_plan=None,
    financial_statement=None,
    tax_return=None,
    memorandum_of_association=None,
):
    try:

        result = await db.execute(
            select(Case).where(Case.id == case_id)
        )

        case = result.scalar_one_or_none()

        if not case:
            raise HTTPException(status_code=404, detail="Case not found")

        # Update fields
        if customer_name:
            case.customer_name = customer_name

        if mobile_number:
            case.mobile_number = mobile_number

        if email:
            case.email = email

        if employer_name:
            case.company_name = employer_name

        if emirates_id:
            case.emirates_id = emirates_id

        if monthly_salary:
            case.salary = monthly_salary

        if requested_amount:
            case.requested_amount = requested_amount

        if status:
            case.status = status

        # Get case documents
        doc_result = await db.execute(
            select(CaseDocument).where(CaseDocument.case_id == case_id)
        )

        documents = doc_result.scalar_one_or_none()

        if not documents:
            documents = CaseDocument(case_id=case_id)
            db.add(documents)

        # Upload files only if provided
        if emirates_id_front:
            documents.emirates_id_front_url = await save_upload_file(emirates_id_front, f"cases/{case_id}")

        if emirates_id_back:
            documents.emirates_id_back_url = await save_upload_file(emirates_id_back, f"cases/{case_id}")

        if passport_copy:
            documents.passport_copy_url = await save_upload_file(passport_copy, f"cases/{case_id}")

        if residence_visa:
            documents.residencevisa_url = await save_upload_file(residence_visa, f"cases/{case_id}")

        if salary_certificate:
            documents.salary_certificate_url = await save_upload_file(salary_certificate, f"cases/{case_id}")

        if bank_statement_last_3_months:
            documents.bank_statement_last_3_months_url = await save_upload_file(bank_statement_last_3_months, f"cases/{case_id}")

        if bank_statement_last_6_months:
            documents.bank_statement_last_6_months_url = await save_upload_file(bank_statement_last_6_months, f"cases/{case_id}")

        if trade_license:
            documents.trade_license_url = await save_upload_file(trade_license, f"cases/{case_id}")

        if liability_letter:
            documents.liability_letter_url = await save_upload_file(liability_letter, f"cases/{case_id}")

        if noc_from_employer:
            documents.noc_from_employer_url = await save_upload_file(noc_from_employer, f"cases/{case_id}")

        if security_cheque:
            documents.security_cheque_url = await save_upload_file(security_cheque, f"cases/{case_id}")

        if utility_bill:
            documents.utility_bill_url = await save_upload_file(utility_bill, f"cases/{case_id}")

        if tenancy_contract:
            documents.tenancy_contract_url = await save_upload_file(tenancy_contract, f"cases/{case_id}")

        if proof_of_address:
            documents.proof_of_address_url = await save_upload_file(proof_of_address, f"cases/{case_id}")

        if last_3_month_payslips:
            documents.last_3_month_payslips_url = await save_upload_file(last_3_month_payslips, f"cases/{case_id}")

        if last_6_month_payslips:
            documents.last_6_month_payslips_url = await save_upload_file(last_6_month_payslips, f"cases/{case_id}")

        if company_id_card:
            documents.company_id_card_url = await save_upload_file(company_id_card, f"cases/{case_id}")

        if labor_contract:
            documents.labor_contract_url = await save_upload_file(labor_contract, f"cases/{case_id}")

        if employment_letter:
            documents.employment_letter_url = await save_upload_file(employment_letter, f"cases/{case_id}")

        if bank_account_statement:
            documents.bank_account_statement_url = await save_upload_file(bank_account_statement, f"cases/{case_id}")

        if credit_report:
            documents.credit_report_url = await save_upload_file(credit_report, f"cases/{case_id}")

        if existing_loan_statement:
            documents.existing_loan_statement_url = await save_upload_file(existing_loan_statement, f"cases/{case_id}")

        if property_document:
            documents.property_document_url = await save_upload_file(property_document, f"cases/{case_id}")

        if vehicle_registration:
            documents.vehicle_registration_url = await save_upload_file(vehicle_registration, f"cases/{case_id}")

        if business_plan:
            documents.business_plan_url = await save_upload_file(business_plan, f"cases/{case_id}")

        if financial_statement:
            documents.financial_statement_url = await save_upload_file(financial_statement, f"cases/{case_id}")

        if tax_return:
            documents.tax_return_url = await save_upload_file(tax_return, f"cases/{case_id}")

        if memorandum_of_association:
            documents.memorandum_of_association_url = await save_upload_file(memorandum_of_association, f"cases/{case_id}")

        await db.commit()

        return {
            "message": "Case updated successfully",
            "case_id": case_id
        }

    except Exception as e:
        await db.rollback()
        raise e


async def get_my_cases(
    db,
    user,
    page: int = 1,
    limit: int = 10,
    search: str | None = None
):

    offset = (page - 1) * limit

    query = select(Case).where(Case.agent_id == user.id)

    if search:
        query = query.where(
            or_(
                Case.customer_name.ilike(f"%{search}%"),
                Case.mobile_number.ilike(f"%{search}%"),
                Case.email.ilike(f"%{search}%"),
                Case.passport_no.ilike(f"%{search}%"),
                Case.emirates_id.ilike(f"%{search}%")
            )
        )

    # total count
    total_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(total_query)
    total = total_result.scalar()

    # pagination
    result = await db.execute(
        query.offset(offset).limit(limit)
    )

    cases = result.scalars().all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": cases
    }