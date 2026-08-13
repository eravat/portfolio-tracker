from fastapi import Depends, HTTPException, APIRouter
from database_models.users_model import Users
from sqlalchemy.orm import Session
from models import CreateUser, LoginUser
from services.auth_service import password_hasher, check_password, create_access_token, get_current_user, get_db
from datetime import timedelta

router = APIRouter(prefix="/auth")

@router.post("/register")
def register(user: CreateUser, db: Session = Depends(get_db)):
    hashed = password_hasher(user.password)
    new_user = Users(email=user.email, hashed_password=hashed)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except:
        raise HTTPException(status_code=409, detail="Email has already been entered.")
    return new_user
    
@router.post("/login")
def login(user: LoginUser, db: Session = Depends(get_db)):
    user_profile = db.query(Users).filter(Users.email==user.email).first()

    if user_profile and check_password(user.password, user_profile.hashed_password) == True:
        token = create_access_token(user_profile.id, timedelta(minutes=30)) 
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Incorrect email or password")   #changed to an exception so client model knows request was not correctly answered

@router.get("/info")
def get_user_info(current_user: Users = Depends(get_current_user)):
    return current_user