from typing import Optional, List
from fastapi import APIRouter, Query, Body, Depends

from pydantic import BaseModel, Field
import datetime

from app.routers.dependencies.request import BookRequestCreate, BookResponseCreate

router = APIRouter(
    responses={
        200: {"description": "Ok"},
        201: {"description": "creation"},
        400: {"description": "Bad Request"},
        404: {"description": "Not found"},
    },
)


class ResponseBookInfo(BaseModel):
    """
    요청된 책을 응답하는데 있어서의 필수 정보
    """

    isbn: str = Field(
        ...,
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=11,
        regex="^[0-9-]{11,}",
        examples={
            "only_number": {"value": {"isbn": "9788966261840"}},
            "include_hippen": {"value": {"isbn": "979-11-6254-196-8"}},
        },
    )
    title: str = Field(title="title", description="책의 제목")
    date: datetime.datetime = Field(title="date", description="책의 정보가 저장된 시간")


@router.post("/")
async def request(
    book: BookRequestCreate = Body(
        ...,
        title="book",
        description="요청 하는 책의 필요 데이터",
        examples={
            "only_number": {"value": {"isbn": "9788966261840"}},
            "include_hippen": {"value": {"isbn": "979-11-6254-196-8"}},
        },
    )
):
    """
    외부 API를 이용하여(하루 5천회 사용가능) 내부 DB에 결과값을 저장합니다.
    json body를 통해 식별합니다.
    """
    book.date = book.date or datetime.datetime.now()

    # TODO: 내부 저장 후 요청 id 출력
    return {"request": book}


@router.post("/list")
async def request(
    books: List[BookRequestCreate] = Body(
        ...,
        title="book",
        description="요청 하는 책의 필요 데이터들",
        example=[{"isbn": "9788966261840"}, {"isbn": "979-11-6254-196-8"}],
    )
):
    """
    외부 API를 이용하여(하루 5천회 사용가능) 내부 DB에 결과값을 저장합니다.
    단, 리스트를 통해 한번에 여러개의 요청을 받습니다. (최대 1000개)
    """

    def fill_date(x):
        x.date = x.date or datetime.datetime.now()
        return x

    books = list(map(fill_date, books))
    return books
