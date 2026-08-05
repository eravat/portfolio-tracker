from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql://postgres:MzoAf6hb7@localhost:5432/ebrahim"
engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)