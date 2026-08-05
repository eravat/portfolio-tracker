import requests
from config import API_KEY
from fastapi import FastAPI
from database import session, engine
import users_models
from sqlalchemy.orm import Session

app = FastAPI()

users_models.Base.metadata.create_all(bind=engine)      #creates users tables

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

