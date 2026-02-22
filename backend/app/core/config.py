from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    PROJECT_NAME: str = "Rotiseria API"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./rotiseria.db"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    ALGORITHM: str = "HS256"

settings = Settings()

db_url = os.getenv("DATABASE_URL")
if db_url:
    settings.SQLALCHEMY_DATABASE_URI = db_url