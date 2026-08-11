from pydantic import BaseModel
from datetime import date
from decimal import Decimal

class CreateUser(BaseModel):
    email: str
    hashed_password: str

class LoginUser(BaseModel):
    email: str
    password: str

class CreatePortfolio(BaseModel):
    portfolio_name: str

class CreateTransaction(BaseModel):
    ticker: str
    quantity: Decimal
    price: Decimal
    type: str
    transaction_date: date
