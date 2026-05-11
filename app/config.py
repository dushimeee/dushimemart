"""
DushimeMart - Application Configuration
Author: Cleonide Dushime (ID: 70871)
Loads configuration from environment variables (.env file).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    SECRET_KEY: str = "fallback-key-please-set-env"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str = "sqlite:///./dushimemart.db"
    ALGORITHM: str = "HS256"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
