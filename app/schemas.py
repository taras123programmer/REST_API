from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Book(BaseModel):
    id : int
    author : str
    title : str
    text : str