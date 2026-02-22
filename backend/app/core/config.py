from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Rotiseria API"
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:5173"]
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///./rotiseria.db"
    SECRET_KEY: str = "changeme"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
