from os import getenv

class Config:
    USERNAME = 'postgres'
    PASSWORD = 'password'
    DATABASE = 'BooksDB'
    HOST = getenv("DB_HOST", "localhost")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:5432/{DATABASE}?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False