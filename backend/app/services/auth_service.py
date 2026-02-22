from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate
from ..core.security import get_password_hash, verify_password, create_access_token


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        business_id=user_in.business_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_token_for_user(user: User) -> str:
    data = {
        "sub": str(user.id),              # ← CLAVE
        "business_id": user.business_id
    }
    return create_access_token(data)