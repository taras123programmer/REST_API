import os
from pydantic_settings import BaseSettings

USERNAME = 'postgres'
PASSWORD = 'password'
DATABASE = 'booksdb'
HOST = os.getenv("DB_HOST", "localhost")

class Settings(BaseSettings):

    SQLALCHEMY_DATABASE_URL : str = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}"
    SECRET_KEY: str = "mysecretkey"
    REFRESH_SECRET_KEY: str = "mysecretkey1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

settings = Settings()