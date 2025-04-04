import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import settings
from app.models import User
from sqlalchemy.orm import Session
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def refresh_access_token(refresh_token):
    data = verify_token(refresh_token, settings.REFRESH_SECRET_KEY)
    if data:
        return create_access_token(data)
    else:
        return False

def login(db : Session, username : str, password : str):
    user = db.query(User).filter_by(username = username).first()
    if user and verify_password(password, user.password):
        return True
    else:
        return False

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_token(token: str, secret_key=settings.SECRET_KEY):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token has expired")
    except PyJWTError:
        raise HTTPException(401, detail="Invalid token")

