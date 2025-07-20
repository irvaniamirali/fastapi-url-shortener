from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or a .env file.
    """
    PROJECT_NAME: str = "FastAPI URL Shortener"
    DESCRIPTION: str = "FastAPI URL Shortener"
    VERSION: str = "0.1.0"

    DATABASE_URL: str = "sqlite+aiosqlite:///./shortener.db"
    DATABASE_ECHO: bool = False

    BASE_DOMAIN: str = "http://localhost:8000"

    SECRET_KEY: str = "your-super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging settings
    LOG_LEVEL: str = "INFO"

    # Redis settings for Rate Limiting
    REDIS_URL: str = "redis://localhost:6379/0"

    # Rate Limiting settings
    RATE_LIMIT_REGISTER_TIMES: int = 5
    RATE_LIMIT_REGISTER_SECONDS: int = 60

    RATE_LIMIT_LOGIN_TIMES: int = 10
    RATE_LIMIT_LOGIN_SECONDS: int = 60

    RATE_LIMIT_CREATE_URL_TIMES: int = 20
    RATE_LIMIT_CREATE_URL_SECONDS: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
