from typing import Optional, List
from fastapi import APIRouter, Query, Body

from pydantic import BaseModel, Field
import datetime


router = APIRouter(
    prefix="/api/v1/request",
    tags=["search"],
    responses={
        200: {"description": "Ok"},
        201: {"description": "creation"},
        400: {"description": "Bad Request"},
        404: {"description": "Not found"},
    },
)


class RequsetBookInfo(BaseModel):
    """
    책을 요청하는데 필요한 정보
    """

    isbn: str = Field(
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        examples={
            "only_number": "9788966261840",
            "include_hippen": "979-11-6254-196-8",
        },
    )


class RequestAcceptedBookInfo(BaseModel):
    """
    요청에 대한 응답
    """

    isbn: str = Field(
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        examples={
            "only_number": "9788966261840",
            "include_hippen": "979-11-6254-196-8",
        },
    )
    date: datetime.datetime = Field(title="date", description="요청을 받은 날짜 및 시간")


class ResponseBookInfo(BaseModel):
    """
    요청된 책을 응답하는데 있어서의 필 수 정보
    """

    isbn: str = Field(
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        examples={
            "only_number": "9788966261840",
            "include_hippen": "979-11-6254-196-8",
        },
    )
    title: str = Field(title="title", description="책의 제목")
    date: datetime.datetime = Field(title="date", description="책의 정보가 저장된 시간")


@router.post("/")
async def request(books: List[RequsetBookInfo] = Body(...)):
    """
    외부 API를 이용하여(하루 5천회 사용가능) 내부 DB에 결과값을 저장합니다.
    """
    pass
