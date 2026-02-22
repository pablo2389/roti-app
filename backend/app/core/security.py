from datetime import datetime, timedelta
from typing import Optional
import hashlib
import hmac
from jose import jwt, JWTError
from ..core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    salt = settings.SECRET_KEY.encode()
    dk = hashlib.pbkdf2_hmac('sha256', plain_password.encode(), salt, 100000)
    return hmac.compare_digest(dk.hex(), hashed_password)


def get_password_hash(password: str) -> str:
    salt = settings.SECRET_KEY.encode()
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return dk.hex()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise
