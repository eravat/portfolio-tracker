import requests
from config import API_KEY
from fastapi import FastAPI, Depends
from database import session, engine
from users_models import Users, UserBase
from sqlalchemy.orm import Session
import bcrypt
from models import CreateUser

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

def password_hasher(original_password: str):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password=original_password.encode('utf-8'), salt=salt)
    return hash_password.decode('utf-8')

def check_password(user_password_input: str, hash_password: str):
    check = bcrypt.checkpw(password=user_password_input.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))   #need to fetch hashed password from database based on email entered
    return check

#def get_hashed_password_by_email(email: str, db: Session):
#    db_hashed_password = db.query(Users).filter(Users.email==email).first().hashed_password
#    return db_hashed_password 

@app.post("/auth/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    user.hashed_password = password_hasher(user.hashed_password)
    db.add(Users(**user.model_dump()))
    db.commit()
    return user
    


@app.post("/auth/login")
def login(user: CreateUser, db: Session = Depends(get_db)):
    user_profile = db.query(Users).filter(Users.email==user.email).first()
    if user_profile:
        check = check_password(user.hashed_password, user_profile.hashed_password)  #the user.hashed_password isn't actually a hashed password yet
        return check
    return "no matching email found"
        


