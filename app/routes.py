from fastapi import *
from app.models import Book

book_router = APIRouter(prefix='/book')

books = [
    {'id':1,'title':'Book 1', 'author':'Author 1', 'text':'Text 1'},
    {'id':2,'title':'Book 2', 'author':'Author 2', 'text':'Text 2'},
    {'id':3,'title':'Book 3', 'author':'Author 3', 'text':'Text 3'},
    {'id':4,'title':'Book 4', 'author':'Author 4', 'text':'Text 4'}
]

@book_router.get('/{id}')
async def get_book(response:Response, id:int):
    res = [book for book in books if book['id'] == id]
    if res:
        return res[0]
    else:
        response.status_code = status.HTTP_404_NOT_FOUND
        return None

@book_router.get('/')
async def get_all_book():
    books_list = [Book.model_validate(book) for book in books]
    return books_list

@book_router.post('/')
async def add_book(response:Response, book : Book):
    books.append(book.model_dump())
    response.status_code = 201
    return None

@book_router.delete('/{id}')
async def delete_book(response:Response, id:int):
    for b in books:
        if b['id'] == id:
            books.remove(b)
            response.status_code = 204
            break
    else:
        response.status_code = 404

    return None