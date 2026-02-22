from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from ..core.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    business_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
