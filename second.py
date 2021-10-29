from fastapi import FastAPI, Path, Query, Body, Cookie, Header
from typing import Optional, List
from pydantic import BaseModel, Field
import datetime
from second_util import query_and_register

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter
@app.get("/isbn/{isbn}")
async def search_isbn(
    isbn: str = Path(
        ..., title="book isbn, length will be 13", min_length=13, max_length=13
    )
):
    return {"isbn": isbn}


# query parameter
@app.get("/search")
async def search(
    isbn: Optional[str] = Query(
        None,
        title="isbn 넘버",
        description="책을 isbn으로 검색합니다. 13자리 isbn을 사용합니다.",
        min_legnth=13,
        max_length=13,
    ),
    title: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="title search(option)",
        description="제목으로 검색합니다. 단, 한글자는 필요합니다.",
    ),
):
    result = {"result": "not implemented"}
    return result


# meet pydantic
class RequestBookInfo(BaseModel):
    isbn: str = Field(..., regex=r"^[0-9]{13}$", example="9788966261840")
    title: Optional[str] = Field(None, example="Two Scopoops of Django")
    date: datetime.datetime = Field(None, example=datetime.datetime.now())


class ResponseBookInfo(BaseModel):
    isbn: str = Field(..., example="9788966261840")
    title: str = Field(..., example="Two Scopoops of Django")


# @app.get("/request", response_model=ResponseBookInfo)
@app.get("/request")
async def request_book(
    isbn: List[str] = Query(..., regex="^[0-9]{13}$", example="9788966261840")
):
    """한개의 isbn 혹은 여러개의 isbn을 get, query로 받습니다
    받은 isbn은 개인 DB에 없으면 알라딘API를 이용해 정보를 등록합니다.
    """
    response = {}
    for i in isbn:
        book, status = await query_and_register(i)
        response[i] = [book["title"], status]

    return response


#
@app.post("/request")
async def request_book(
    book: List[RequestBookInfo] = Body(..., example={"isbn": "9788966261840"})
):
    """처리할 isbn정보를 post로 받는 함수
    받은 isbn은 개인 DB에 없으면 알라딘API를 이용해 정보를 등록합니다.
    # TODO: 어떻게 여러개의 isbn을 받을 것인지 연구
    """
    book.date = datetime.datetime.now()
    return book
