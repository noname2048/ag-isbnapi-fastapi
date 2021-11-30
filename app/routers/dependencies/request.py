import datetime
from fastapi import Query


class BookRequestParams:
    def __init__(self, isbn: str = Query(), date=Query(None)):
        self.isbn = isbn
        self.date = date or datetime.datetime.now()
