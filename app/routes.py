from fastapi import *
from app.models import Book
from bson import ObjectId
from bson.errors import InvalidId
from database import get_db
from sqlalchemy.orm import Session

book_router = APIRouter(prefix='/book')

@book_router.get('/{id}')
async def get_book(id:str, db: Session = Depends(get_db)):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400)

    res = await db.query(Book).filter_by(id = id)
    if res:
        res['id'] = str(res.pop('_id'))
        return res
    else:
        raise HTTPException(status_code=404)

@book_router.get('/')
async def get_all_book():
    res = await books.find().to_list(None)
    return [{'id' : str(book.pop('_id')), **book} for book in res]

@book_router.post('/')
async def add_book(response:Response, book : Book):
    res = await books.insert_one(book.model_dump())
    response.status_code = 201
    return {'id' : str(res.inserted_id)}

@book_router.delete('/{id}')
async def delete_book(response:Response, id:str):
    try:
        object_id = ObjectId(id)
    except InvalidId:
        raise HTTPException(status_code=400)

    res = await books.delete_one({'_id' : object_id})
    if res.deleted_count == 1:
        response.status_code = 204
        return None
    else:
        raise HTTPException(404)