from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import Settings

engine = create_engine(Settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

