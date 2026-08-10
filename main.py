import requests
from config import API_KEY
from fastapi import FastAPI, Depends, HTTPException
from database import engine, UserBase
from database_models.users_model import Users
from database_models.portfolios_model import Portfolios
from database_models.transactions_model import Transactions
from sqlalchemy.orm import Session
from models import CreateUser, LoginUser
from auth import password_hasher, check_password, create_access_token, get_current_user, get_db
from datetime import timedelta


app = FastAPI()

UserBase.metadata.create_all(bind=engine)      #creates users tables


@app.get("/")
def greet():
    return "Portfolio Tracker"


def get_stock(ticker: str):
    response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=15min&apikey={API_KEY}")
    data = response.json()
    return data["Global Quote"]


def get_price(ticker: str):    
    return get_stock(ticker)["05. price"]


@app.post("/auth/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    user.hashed_password = password_hasher(user.hashed_password)
    db.add(Users(**user.model_dump()))
    db.commit()
    return user
    
@app.post("/auth/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    user_profile = db.query(Users).filter(Users.email==user.email).first()

    if user_profile and check_password(user.password, user_profile.hashed_password) == True:
        token = create_access_token(user_profile.id, timedelta(minutes=30)) 
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="incorrect email or password")   #changed to an exception so client model knows request was not correctly answered

@app.get("/auth/info")
def get_user_info(current_user: Users = Depends(get_current_user)):
    return current_user




