from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    PROJECT_NAME: str = "Rotiseria API"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./rotiseria.db"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week
    ALGORITHM: str = "HS256"


settings = Settings()

# Allow platforms (Render) that provide DATABASE_URL to override the SQLALCHEMY URI
db_url = os.getenv("DATABASE_URL")
if db_url:
    # Render/Heroku-style DATABASE_URL may be provided; prefer it when present
    settings.SQLALCHEMY_DATABASE_URI = db_url
