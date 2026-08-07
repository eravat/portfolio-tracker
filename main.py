import requests
from config import API_KEY
from fastapi import FastAPI, Depends, HTTPException
from database import session, engine
from users_models import Users, UserBase
from sqlalchemy.orm import Session
import bcrypt
from models import CreateUser, LoginUser
from auth import password_hasher, check_password, create_access_token

app = FastAPI()

UserBase.metadata.create_all(bind=engine)      #creates users tables

def get_db():
    db = session()
    try:
        yield db        #waiting for the other function to use it
    finally:
        db.close()


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
        return True
    raise HTTPException(status_code=401, detail="incorrect email or password")   #changed to an exception so client model knows request was not correctly answered
        


