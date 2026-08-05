from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Users(Base):

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)      #don't need to index because pks are indexed automatically
    email = Column(String, index=True)          #often need to find email so indexing speeds up read time
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
