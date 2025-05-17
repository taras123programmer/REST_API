from fastapi import *
from app.models import Book
from app.database import get_db
from app.rate_limit import rate_limit
from app.schemas import BookSchema
from app.auth_service import *
from fastapi.security import OAuth2PasswordBearer

book_router = APIRouter(prefix='/book')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
oauth2_scheme_not_required = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

@book_router.get('/{id}', response_model=BookSchema)
async def get_book(id:int, request:Request, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme_not_required)):
    #Токен не обов'язковий, але із токеном більший rate limit
    if token:
        username = verify_token(token)['username']
        await rate_limit(request, username)
    else:
        await rate_limit(request, None)

    book = db.query(Book).filter_by(id = id).first()
    if book:
        return book
    else:
        raise HTTPException(status_code=404)

@book_router.get('/')
async def get_all_book(request:Request, db: Session = Depends(get_db),
                       token: str = Depends(oauth2_scheme_not_required), limit:int=None, cursor:int=None):

    if token:
        username = verify_token(token)['username']
        await rate_limit(request, username)
    else:
        await rate_limit(request, None)

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
async def add_book(request:Request, response:Response, book : BookSchema,
                   db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    # Токен обов'язковий, для методів що вносять зміни
    username = verify_token(token)['username']
    await rate_limit(request, username)

    book_model = Book(author=book.author, title=book.title, text=book.text)
    db.add(book_model)
    db.commit()

    response.status_code = 201
    return {'id' : book_model.id}

@book_router.delete('/{id}')
async def delete_book(request:Request, response:Response, id:int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    username = verify_token(token)['username']
    await rate_limit(request, username)

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
async def get_token(request:Request, username:str=None, password:str=None, db: Session = Depends(get_db)):
    await rate_limit(request, None)

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
async def refresh_token(request:Request, refresh_token:str):
    await rate_limit(request, None)

    access_token = refresh_access_token(refresh_token)
    if access_token:
        return access_token
    else:
        raise HTTPException(401)
