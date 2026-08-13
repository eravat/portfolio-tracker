import requests
from config import API_KEY

def get_stock(ticker: str):
    response = requests.get(f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&interval=15min&apikey={API_KEY}")
    data = response.json()
    return data["Global Quote"]

def get_price(ticker: str):    
    return get_stock(ticker)["05. price"]

cache = {}
