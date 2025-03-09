from fastapi import  FastAPI
from app.routes import book_router

def create_app():
    app = FastAPI()
    app.include_router(book_router)

    return app