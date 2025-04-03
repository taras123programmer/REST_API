from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class BookSchema(BaseModel):
    id : int
    author : str
    title : str
    text : str

    class Config:
        orm_mode = True