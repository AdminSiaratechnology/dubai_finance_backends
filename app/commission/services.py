from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.commission.models import Bank, LoanType
from app.commission.schemas import LoanCreate,LoanTypeOut


################# Loan Type ###################
async def create_loan_type(session: AsyncSession, loantype:LoanCreate) -> LoanTypeOut:
  loantype = LoanType(name=loantype.name)
  session.add(loantype)
  await session.commit()
  await session.refresh(loantype)
  return loantype
