import os
from dotenv import load_dotenv

# Automatically load test env if running pytest
if os.getenv("PYTEST_CURRENT_TEST"):
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        ...,  # Required
        env="DATABASE_URL"
    )
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DEBUG: bool = Field(default=False, env="DEBUG")
    API_URL: str = Field(..., env="API_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()