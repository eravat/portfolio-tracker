from fastapi import HTTPException, APIRouter
from datetime import datetime
from services.pricing_service import get_price, cache


router = APIRouter(prefix="/stocks")

@router.get("/{ticker}/price")
def get_stock_price(ticker: str):
    try:
        if ticker in cache and ((datetime.now() - cache[ticker][1]).total_seconds() // 60) < 10:        #checking if ticker price is already stored in cache and is relatively new (within 10 minutes)
            price = float(cache[ticker][0])
        else:
            price = float(get_price(ticker))
            cache[ticker] = [price, datetime.now()]
    except KeyError:
        raise HTTPException(status_code=404, detail="Ticker not found")
    
    return price
