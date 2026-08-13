from database_models.users_model import Users
from database_models.portfolios_model import Portfolios
from sqlalchemy.orm import Session
from models import CreatePortfolio
from services.auth_service import get_current_user, get_db
from fastapi import Depends, APIRouter




router = APIRouter(prefix="/portfolios")

@router.post("")
def add_portfolio(user_portfolio: CreatePortfolio, current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    new_portfolio = Portfolios(portfolio_name=user_portfolio.portfolio_name, user_id=current_user.id)
    db.add(new_portfolio)
    db.commit()
    db.refresh(new_portfolio)
    return new_portfolio

@router.get("")
def get_portfolios(current_user: Users = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolios = db.query(Portfolios).filter(current_user.id==Portfolios.user_id).all()
    return portfolios