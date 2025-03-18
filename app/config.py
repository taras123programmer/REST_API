class Config:
    USERNAME = 'postgres'
    PASSWORD = 'password'
    DATABASE = 'booksdb'
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@localhost:5432/{DATABASE}?client_encoding=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False