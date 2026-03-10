from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.config import SessionDep
from app.account.deps import get_current_user
from app.account.models import User
from app.Lead.SubmitCase.services import submit_complete_case

router = APIRouter()


@router.post("/submit-complete")
async def submit_complete_case_router(
    session: SessionDep,
    user: User = Depends(get_current_user),

    customer_name: str = Form(...),
    mobile_number: str = Form(...),
    email: str = Form(...),
    employer_name: str = Form(...),
    monthly_salary: float = Form(...),
    bank_id: int = Form(...),
    product_id: int = Form(...),
    requested_amount: float = Form(...),

    emirates_id_front: UploadFile | None = File(None),
    emirates_id_back: UploadFile | None = File(None),
    passport_copy: UploadFile | None = File(None),
    residence_visa: UploadFile | None = File(None),
):
    
    return await submit_complete_case(
        session,
        user.id,
        customer_name,
        mobile_number,
        email,
        employer_name,
        monthly_salary,
        bank_id,
        product_id,
        requested_amount,
        emirates_id_front,
        emirates_id_back,
        passport_copy,
        residence_visa
    )