from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class BookSchema(BaseModel):
    id : Optional[int] = None
    author : str
    title : str
    text : str

    class Config:
        from_attributes = True