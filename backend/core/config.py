import os
from dotenv import load_dotenv

# Choose the appropriate env file
if os.getenv("DOCKER") == "true":
    load_dotenv(".env.docker")
elif os.getenv("PYTEST_CURRENT_TEST"):
    load_dotenv(".env.test")
else:
    load_dotenv(".env")

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    DEBUG: bool = Field(default=False, env="DEBUG")
    API_URL: str = Field(..., env="API_URL")

    class Config:
        env_file_encoding = "utf-8"

settings = Settings()
