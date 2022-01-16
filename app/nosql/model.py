from odmantic import EmbeddedModel, Model
from typing import Optional, List, Any
from datetime import datetime


class Response(EmbeddedModel):
    isbn13: int
    created_at: datetime

    success: bool
    detail: Any

    class Config:
        collection = "responses"


class Request(Model):
    isbn13: int
    created_at: datetime
    response: Response

    class Config:
        collection = "requests"


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

    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        collection = "books"
