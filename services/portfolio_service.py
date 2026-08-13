from fastapi import HTTPException
from database_models.users_model import Users
from database_models.portfolios_model import Portfolios
from sqlalchemy.orm import Session

def check_portfolio(portfolio_id: int, current_user: Users, db: Session):
    portfolio = db.query(Portfolios).filter(portfolio_id==Portfolios.id).first()  #this function prevents invalid portfolio ids from being input by client
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    if portfolio.user_id != current_user.id:
        raise HTTPException(status_code=406, detail="Invalid portfolio id")
    return portfolio