import datetime
from pydantic import BaseModel


class BookBase(BaseModel):
    isbn: int
    date: datetime.datetime = None


class BookRequestCreate(BookBase):
    pass


class BookRequest(BookRequestCreate):
    id: int


class BookResponseCreate(BookBase):
    request_id: int


class BookResponse(BookResponseCreate):
    id: int
