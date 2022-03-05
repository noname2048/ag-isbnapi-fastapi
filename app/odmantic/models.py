from typing import Optional
from odmantic import Model
from datetime import datetime


class Request(Model):
    isbn: str
    created_date: datetime
    updated_date: datetime
    status: str

    class Config:
        collection = "requests"


class Book(Model):
    title: str
    description: Optional[str]
    isbn13: int
    cover: str
    publisher: str
    price: int
    pub_date: datetime
    author: str

    created_at: datetime
    updated_at: datetime

    class Config:
        collection = "books"
