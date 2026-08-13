from fastapi import FastAPI
from routers.auth import router as auth_router
from routers.portfolios import router as portfolios_router
from routers.transactions import router as transactions_router
from routers.holdings import router as holdings_router
from routers.stocks import router as stocks_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(portfolios_router)
app.include_router(transactions_router)
app.include_router(holdings_router)
app.include_router(stocks_router)
















