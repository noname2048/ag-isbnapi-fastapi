from typing import Collection, Optional, Union
from odmantic import Model
from datetime import datetime


class TimeStampModel(Model):
    created_at: datetime
    updated_at: datetime


class Request(Model):
    # id(str) will default
    isbn13: int
    state_code: int

    response_type: Optional[str]  # error, book
    response_id: Optional[int]

    created_at: datetime
    answered_at: Union[datetime, None]

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


class ErrorReport(Model):
    # id(str) will default
    isbn13: int
    request_id: str
    created_at: datetime
    data: Optional[Union[dict, str]]

    class Config:
        collection = "errors"
