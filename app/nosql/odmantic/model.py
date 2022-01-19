from bson import ObjectId

from odmantic import EmbeddedModel, Model
from typing import Optional, List, Any
from datetime import datetime


class Request(Model):
    isbn13: int
    created_at: datetime
    response_id: Optional[ObjectId]

    class Config:
        collection = "requests"


class Response(Model):
    isbn13: int
    created_at: datetime
    request_id: ObjectId

    success: Optional[bool]
    detail: Any

    class Config:
        collection = "responses"


class Book(Model):
    # id(str) will default
    title: str
    description: Optional[str]
    isbn13: int
    cover: str
    publisher: str
    price: int
    pub_date: datetime
    author: str
    response_id: ObjectId

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        collection = "books"
