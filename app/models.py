from pydantic import BaseModel
from bson import ObjectId
from typing import Optional

class Book(BaseModel):
    id : Optional[str] = None
    author : str
    title : str
    text : str

    class Config:
        json_encoders = {ObjectId: str}