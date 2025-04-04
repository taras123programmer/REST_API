from fastapi import *
from app.models import Book
from app.database import get_db
from sqlalchemy.orm import Session
from app.schemas import BookSchema
from app.auth_service import *
from fastapi.security import OAuth2PasswordBearer

book_router = APIRouter(prefix='/book')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

@book_router.get('/{id}', response_model=BookSchema)
async def get_book(id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    book = db.query(Book).filter_by(id = id).first()
    if book:
        return book
    else:
        raise HTTPException(status_code=404)

@book_router.get('/')
async def get_all_book(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), limit:int=None, cursor:int=None):
    verify_token(token)
    if not limit:
        limit = 10
    if cursor:
        books = db.query(Book).filter(Book.id > cursor).limit(limit).all()
    else:
        books = db.query(Book).limit(limit).all()

    if not books:
        raise HTTPException(status_code=404)

    cursor = books[-1].id

    return {'books' : [BookSchema.from_orm(book) for book in books], 'cursor' : cursor}

@book_router.post('/')
async def add_book(response:Response, book : BookSchema, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    book_model = Book(author=book.author, title=book.title, text=book.text)
    db.add(book_model)
    db.commit()
    response.status_code = 201
    return {'id' : book_model.id}

@book_router.delete('/{id}')
async def delete_book(response:Response, id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    book = db.query(Book).filter_by(id = id).first()
    if book:
        db.delete(book)
        db.commit()
        response.status_code = 204
        return None
    else:
        raise HTTPException(404)


token_router = APIRouter(prefix='/token')

@token_router.get('/')
async def get_token(username:str=None, password:str=None, db: Session = Depends(get_db)):
    if username and password:
        if login(db, username, password):
            refresh_token = create_refresh_token({'username': username})
            access_token = create_access_token({'username' : username})
            return {'refresh_token' : refresh_token, 'access_token' : access_token}
        else:
            raise HTTPException(401)
    else:
        raise  HTTPException(400)

@token_router.get('/access_token')
async def refresh_token(refresh_token:str, db: Session = Depends(get_db)):
    access_token = refresh_access_token(refresh_token)
    if access_token:
        return access_token
    else:
        raise HTTPException(401)
