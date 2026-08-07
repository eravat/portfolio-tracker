from pydantic import BaseModel

class CreateUser(BaseModel):
    email: str
    hashed_password: str

class LoginUser(BaseModel):
    email: str
    password: str
