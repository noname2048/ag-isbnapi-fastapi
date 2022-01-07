from typing import Collection, Optional
from odmantic import Model
from datetime import datetime


class TimeStampModel(Model):
    created_at: datetime
    updated_at: datetime


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

    created_at: Optional[datetime]

    class Config:
        collection = "books"


class Request(Model):
    # id(str) will default
    isbn13: int
    request_date: datetime
    result_code: int
    response_id: Optional[int]
    response_date: Optional[datetime]

    class Config:
        collection = "requests"


class Response(Model):
    # id(str) will default
    isbn13: int
    response_date: datetime
    request_id: str

    class Config:
        collection = "responses"
