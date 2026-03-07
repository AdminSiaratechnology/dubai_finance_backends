from fastapi import FastAPI
from app.account.routers import router as account_router
from app.loantype.routers.loan_type import router as loan_type_router
from app.category.routers import router as category_router
from app.Bank.routers import router as bank_router
from app.sla_template.routers import router as sla_router
from app.product.routers import router as product_router
from app.commission.routers import router as commission_router
from app.account.analyst.routers import router as analyst_router
from app.account.telecaller.routers import router as telecaller_router
from app.account.agent.routers import router as agent_router
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from fastapi.staticfiles import StaticFiles


app = FastAPI(title="FastAPI Dubai Finance Backend")


app.mount("/media", StaticFiles(directory="media"), name="media")

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
app.include_router(sla_router, prefix="/api/slatemplate", tags=["SLA Template"])
app.include_router(product_router, prefix="/api/product", tags=["Products"])
app.include_router(commission_router, prefix="/api/commission", tags=["Commission"])
app.include_router(analyst_router, prefix="/api/coordinators", tags=["Coordinators"])
app.include_router(telecaller_router, prefix ="/api/telecaller", tags=["Telecallers"])
app.include_router(agent_router, prefix ="/api/agent", tags=["Agents"])