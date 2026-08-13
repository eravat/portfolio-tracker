from fastapi import Depends, HTTPException, APIRouter
from database_models.users_model import Users
from database_models.transactions_model import Transactions
from sqlalchemy.orm import Session
from models import CreateTransaction
from services.auth_service import get_current_user, get_db
from services.portfolio_service import check_portfolio
from services.fifo_service import calculate_ticker_res


router = APIRouter(prefix="/portfolios")

@router.post("/{portfolio_id}/transactions")
def add_transaction(portfolio_id: int, user_transaction: CreateTransaction, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    ticker_res = calculate_ticker_res(db, portfolio_id)
    if user_transaction.type=="sell" and user_transaction.ticker not in ticker_res:
        raise HTTPException(status_code=400, detail="No existing shares available.")
    if user_transaction.type=="sell" and ticker_res[user_transaction.ticker]["total quantity"] < user_transaction.quantity:
        raise HTTPException(status_code=400, detail="Not enough shares available.")
    new_transaction = (Transactions(portfolio_id=portfolio_id, ticker=user_transaction.ticker, quantity=user_transaction.quantity, price=user_transaction.price, type=user_transaction.type, transaction_date=user_transaction.transaction_date))
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction



@router.get("/{portfolio_id}/transactions")
def get_transactions(portfolio_id: int, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    check_portfolio(portfolio_id, current_user, db)
    transactions = db.query(Transactions).filter(portfolio_id==Transactions.portfolio_id).all()
    return transactions