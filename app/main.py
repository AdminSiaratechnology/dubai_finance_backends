from fastapi import FastAPI
from app.account.routers import router as account_router
from app.commission.routers.loan_type import router as loan_type_router
from app.commission.routers.category import router as category_router
from app.commission.routers.bank import router as bank_router
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

app = FastAPI(title="FastAPI Dubai Finance Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Welcome to Finance API"}


app.include_router(account_router, prefix="/api/account", tags=["Account"])
app.include_router(loan_type_router, prefix="/api/loantype", tags=["Loan Type"])
app.include_router(category_router, prefix="/api/category", tags=["Category"])
app.include_router(bank_router, prefix="/api/banks", tags=["Banks"])