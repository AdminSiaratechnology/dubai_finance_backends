from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.commission.models import Bank, LoanType
from app.commission.schemas import LoanCreate,LoanTypeOut


################# Loan Type ###################
async def create_loan_type(session: AsyncSession, loantype:LoanCreate) -> LoanTypeOut:
  # 🔎 Check if already exists
  result = await session.execute(
    select(LoanType).where(LoanType.name == loantype.name)
  )
  existing_loantype = result.scalar_one_or_none()
  if existing_loantype:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Loan type already exists"
        )
  loantype = LoanType(name=loantype.name)
  session.add(loantype)
  await session.commit()
  await session.refresh(loantype)
  return loantype
