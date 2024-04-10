from dotenv import load_dotenv
from pydantic import (
    Field,
)
from pydantic_settings import BaseSettings

load_dotenv()


class Database(BaseSettings):
    path: str = Field(alias="DB_PATH", default="localhost")


class Settings(BaseSettings):
    database: Database = Database()


settings = Settings()
