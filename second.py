from fastapi import FastAPI, Path, Query, Body, Field
from typing import Optional
from pydantic import BaseModel
import datetime

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
    isbn: str = Field(..., regex=r"^[0-9]{13}$")
    title: Optional[str] = None
    date: datetime.datetime = None


@app.post("/request")
async def request_book(book: RequestBookInfo):
    book.date = datetime.datetime.now()
    return book
