from fastapi import Depends, APIRouter
from database_models.users_model import Users
from sqlalchemy.orm import Session
from services.auth_service import get_current_user, get_db
from decimal import Decimal
from services.portfolio_service import check_portfolio
from services.fifo_service import calculate_ticker_res
from services.pricing_service import get_price


router = APIRouter(prefix="/portfolio")

@router.get("/{portfolio_id}/holdings")
def get_holdings(portfolio_id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    
    ticker_res = calculate_ticker_res(db, portfolio_id)
    holdings_ticker_res = {}
    for ticker in ticker_res:
        holdings_ticker_res[ticker] = {"total quantity":ticker_res[ticker]["total quantity"], "average price":ticker_res[ticker]["average price"]}
    return holdings_ticker_res

@router.get("/{portfolio_id}/holdings/pnl")
def get_pnl(portfolio_id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    ticker_res = calculate_ticker_res(db, portfolio_id)
    pnl_ticker_res = {}
    for ticker in ticker_res:       
        current_price = get_price(ticker)
        unrealised_pnl = (Decimal(current_price) - (ticker_res[ticker]["average price"])) * ticker_res[ticker]["total quantity"]
        pnl_ticker_res[ticker] = {"realised pnl":ticker_res[ticker]["realised pnl"], "unrealised pnl":unrealised_pnl}
    return pnl_ticker_res
