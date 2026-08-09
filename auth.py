import bcrypt
from datetime import timedelta, datetime
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from config import SECRET_KEY
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from users_models import Users
from database import session


security = HTTPBearer()

ALGORITHM="HS256"

def get_db():
    db = session()
    try:
        yield db        #waiting for the other function to use it
    finally:
        db.close()

def password_hasher(original_password: str):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password=original_password.encode('utf-8'), salt=salt)
    return hash_password.decode('utf-8')

def check_password(user_password_input: str, hash_password: str):
    check = bcrypt.checkpw(password=user_password_input.encode('utf-8'), hashed_password=hash_password.encode('utf-8'))   #need to fetch hashed password from database based on email entered
    return check

def create_access_token(user_id: str, expires_delta: timedelta | None = None):
    encode = {"sub": str(user_id)}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):

    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Could not validate user")
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user")      

    user = db.query(Users).filter(Users.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Could not validate user")
    return user
