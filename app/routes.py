from fastapi import *
from app.models import Book
from bson import ObjectId
from bson.errors import InvalidId
from database import get_db
from sqlalchemy.orm import Session
from schemas import BookSchema

book_router = APIRouter(prefix='/book')

@book_router.get('/{id}', response_model=BookSchema)
async def get_book(id:int, db: Session = Depends(get_db)):
    book = await db.query(Book).filter_by(id = id).first()
    if book:
        return book
    else:
        raise HTTPException(status_code=404)

@book_router.get('/', response_model=[BookSchema])
async def get_all_book(db: Session = Depends(get_db)):
    books = await db.query(Book).all()
    return books

@book_router.post('/', response_model=BookSchema)
async def add_book(response:Response, book : Book, db: Session = Depends(get_db)):
    book_model = Book(author=book.author, title=book.title, text=book.text)
    db.add(book_model)
    db.commit()
    response.status_code = 201
    return book_model.id

@book_router.delete('/{id}')
async def get_book(response:Response, id:int, db: Session = Depends(get_db)):
    book = await db.query(Book).filter_by(id = id).first()
    if book:
        db.delete(book)
        db.commit()
        response.status_code = 204
        return None
    else:
        raise HTTPException(404)


