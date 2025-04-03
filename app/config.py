import os
from pydantic_settings import BaseSettings

USERNAME = 'postgres'
PASSWORD = 'password'
DATABASE = 'BooksDB'

class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL : str = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE}"
    SECRET_KEY: str = "mysecretkey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()