from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import UserBase

class Portfolios(UserBase):

    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)      
    user_id = Column(Integer, ForeignKey("users.id"))
    portfolio_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())