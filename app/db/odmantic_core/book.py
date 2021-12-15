from odmantic import Field, Model

from typing import Optional
from datetime import datetime as sys_datetime


class Book(Model):
    title: str
    description: Optional[str]
    isbn13: int
    cover: str
    publisher: str
    price: int
    pub_date: sys_datetime
    author: str

    created_at: sys_datetime
    updated_at: Optional[sys_datetime]

    class Config:
        collection = "books"
