import bcrypt
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from jose import jwt, JWTError
from config import SECRET_KEY

ALGORITHM="HS256"

def password_hasher(original_password: str):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password=original_password.encode('utf-8'), salt=salt)
    return hash_password.decode('utf-8')

def check_password(user_password_input: str, hash_password: str):
    check = bcrypt.checkpw(password=user_password_input.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))   #need to fetch hashed password from database based on email entered
    return check

def create_access_token():
    ...                         #not yet completed obviously