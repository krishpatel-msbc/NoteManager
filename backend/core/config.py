from dotenv import load_dotenv
import os

# Load the appropriate .env
if os.getenv("PYTEST_CURRENT_TEST"):
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:password@localhost/notemanager_db",
        env="DATABASE_URL"
    )
    TEST_DATABASE_URL: str = Field(
        default="postgresql+psycopg2://postgres:password@localhost/notemanager_test_db",
        env="TEST_DATABASE_URL"
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
        ...,  # required in .env
        env="API_URL"
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
