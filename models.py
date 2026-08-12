from pydantic import BaseModel, EmailStr, field_validator, Field
from datetime import date
from decimal import Decimal
from typing import Literal

class CreateUser(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one number")
        return value

    
class LoginUser(BaseModel):
    email: EmailStr
    password: str

class CreatePortfolio(BaseModel):
    portfolio_name: str = Field(min_length=1, max_length=50)

class CreateTransaction(BaseModel):
    ticker: str = Field(min_length=1, max_length=10)
    quantity: Decimal = Field(gt=0)
    price: Decimal = Field(gt=0)
    type: Literal["buy", "sell"]
    transaction_date: date

    @field_validator("ticker")
    @classmethod
    def upper_ticker(cls, value):
        return value.upper()

    @field_validator("type", mode="before")
    @classmethod
    def lower_type(cls, value):
        return value.lower()

    @field_validator("transaction_date")
    @classmethod
    def validate_transaction_date(cls, value):
        if value > date.today():
            raise ValueError("Transaction date cannot be set to a future date.")
        return value
