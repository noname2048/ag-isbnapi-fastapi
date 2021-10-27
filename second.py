from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel
import datetime

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# path parameter
@app.get("/isbn/{isbn}")
async def search_isbn(isbn: int = Path(..., title="book isbn, length will be 13")):
    return {"isbn": isbn}


# query parameter
@app.get("/search")
async def search(
    isbn: Optional[int],
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
    isbn: int
    title: Optional[str] = None
    date: datetime.datetime = None


@app.post("/request")
async def request_book(book: RequestBookInfo):
    book.date = datetime.datetime.now()
    return book
