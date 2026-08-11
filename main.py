import requests
from config import API_KEY
from fastapi import FastAPI, Depends, HTTPException
from database import engine, UserBase
from database_models.users_model import Users
from database_models.portfolios_model import Portfolios
from database_models.transactions_model import Transactions
from sqlalchemy.orm import Session
from models import CreateUser, LoginUser, CreatePortfolio, CreateTransaction
from auth import password_hasher, check_password, create_access_token, get_current_user, get_db
from datetime import timedelta, datetime

app = FastAPI()

UserBase.metadata.create_all(bind=engine)      #creates tables

cache = {}

@app.get("/")
def greet():
    return "Portfolio Tracker"

def get_stock(ticker: str):
    response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=15min&apikey={API_KEY}")
    data = response.json()
    return data["Global Quote"]

def get_price(ticker: str):    
    return get_stock(ticker)["05. price"]

def check_portfolio(portfolio_id: int, current_user: Users, db: Session):
    portfolio = db.query(Portfolios).filter(portfolio_id==Portfolios.id).first()  #this function prevents invalid portfolio ids from being input by client
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.user_id != current_user.id:
        raise HTTPException(status_code=406, detail="Invalid portfolio id")
    return portfolio

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

    raise HTTPException(status_code=401, detail="Incorrect email or password")   #changed to an exception so client model knows request was not correctly answered

@app.get("/auth/info")
def get_user_info(current_user: Users = Depends(get_current_user)):
    return current_user

@app.post("/portfolios")
def add_portfolio(user_portfolio: CreatePortfolio, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    new_portfolio = Portfolios(portfolio_name=user_portfolio.portfolio_name, user_id=current_user.id)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio

@app.post("/portfolios/{portfolio_id}/transactions")
def add_transaction(portfolio_id: int, user_transaction: CreateTransaction, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    new_transaction = (Transactions(portfolio_id=portfolio_id, ticker=user_transaction.ticker, quantity=user_transaction.quantity, price=user_transaction.price, type=user_transaction.type, transaction_date=user_transaction.transaction_date))
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@app.get("/portfolios")
def get_portfolios(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolios = db.query(Portfolios).filter(current_user.id==Portfolios.user_id).all()
    return portfolios

@app.get("/portfolios/{portfolio_id}/transactions")
def get_transactions(portfolio_id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    transactions = db.query(Transactions).filter(portfolio_id==Transactions.portfolio_id).all()
    return transactions

@app.get("/stocks/{ticker}/price")
def get_stock_price(ticker: str):
    try:
        if ticker in cache and ((datetime.now() - cache[ticker][1]).total_seconds() // 60) < 10:
            price = float(cache[ticker][0])
        else:
            price = float(get_price(ticker))
            cache[ticker] = [price, datetime.now()]
    except KeyError:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    return price
  
    