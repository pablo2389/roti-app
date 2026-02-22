from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    business_id: Optional[str] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    business_id: Optional[str] = None

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    business_id: Optional[str] = None


class Login(BaseModel):
    email: EmailStr
    password: str
