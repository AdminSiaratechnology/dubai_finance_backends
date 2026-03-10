from sqlalchemy.ext.asyncio import AsyncSession
from app.Lead.SubmitCase.models import Case
from app.Lead.LeadDocuments.models import CaseDocument
from app.loantype.utils import save_upload_file


async def submit_complete_case(
    db: AsyncSession,
    agent_id: int,
    customer_name: str,
    mobile_number: str,
    email: str,
    employer_name: str,
    monthly_salary: float,
    bank_id: int,
    product_id: int,
    requested_amount: float,
    emirates_id_front,
    emirates_id_back,
    passport_copy,
    residence_visa
):

   
    try:

        # create case
        case = Case(
            agent_id=agent_id,
            customer_name=customer_name,
            mobile_number=mobile_number,
            email=email,
            # employer_name=employer_name,
            salary=monthly_salary,
            # bank_id=bank_id,
            # product_id=product_id,
            requested_amount=requested_amount
        )

        db.add(case)
        await db.flush()

        case_id = case.id

        # upload files
        emirates_front_url = await save_upload_file(emirates_id_front, f"cases/{case_id}")
        emirates_back_url = await save_upload_file(emirates_id_back, f"cases/{case_id}")

        documents = CaseDocument(
            case_id=case_id,
            emirates_id_front_url=emirates_front_url,
            emirates_id_back_url=emirates_back_url
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