from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field("postgresql+psycopg2://postgres:wheeling96495@localhost/notemanager_db", env="DATABASE_URL")
    SECRET_KEY: str = Field("supersecret", env="SECRET_KEY")
    DEBUG: bool = Field(True, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

