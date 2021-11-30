import datetime
from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional


class BookRequestParams:
    def __init__(self, isbn: str = Query(...), date=Query(None)):
        self.isbn = isbn
        self.date = date or datetime.datetime.now()


class BookBase(BaseModel):
    isbn: str = Field(
        ...,
        title="isbn(13자리)",
        description="책을 표현하는 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        example="9788966261840",
    )


class BookRequestCreate(BookBase):
    # date: Optional[datetime.datetime] = Field(
    #     None,
    #     title="date",
    #     description="요청시간",
    #     example=datetime.datetime.strptime("2021", "%Y"),
    # )
    pass


class BookResponseCreate(BookBase):
    date: Optional[datetime.datetime] = Field(
        None, title="date", description="정보를 처리한 시간"
    )
