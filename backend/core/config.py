"""
Handles Application configuration using environment variables.
Reads .env file for values such as database URL and secret key.
"""

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """
    Configuration settings loaded from environment or .env file.
    """
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:wheeling96495@localhost/notemanager_db",
        env="DATABASE_URL"
    )
    SECRET_KEY: str = Field(
        default="supersecret",
        env="SECRET_KEY"
    )
    DEBUG: bool = Field(
        default=True,
        env="DEBUG"
    )
    API_URL: str = Field(
        ...,  # no default, require it in .env
        env="API_URL"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create settings instance
settings = Settings()

