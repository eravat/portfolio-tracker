from sqlalchemy import Column, Integer, String, Date, ForeignKey, Numeric
from sqlalchemy.sql import func
from database import UserBase

class Transactions(UserBase):

    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)      
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    ticker = Column(String)
    quantity = Column(Numeric)                                      #using Numeric as floating point can have rounding errors due to its binary approximations
    price = Column(Numeric)
    type = Column(String)
    transaction_date = Column(Date)     #using date because this will be input by user and they may not care about the exact time