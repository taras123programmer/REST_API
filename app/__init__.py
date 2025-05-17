from fastapi import  FastAPI
from redis.asyncio import Redis
from app.routes import book_router, token_router
from app.config import Settings
from app.database import Base, engine, get_db
from app.models import Base
from contextlib import  asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(book_router)
    app.include_router(token_router)

    return app