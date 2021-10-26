from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# path parameter
@app.get("/isbn/{isbn}")
async def search_isbn(isbn: int):
    return {"isbn": isbn}

# query parameter
@app.get("/search")
async def search(isbn: Optional[int], title: Optional[str]):
    pass

# meet pydantic
class RequestBookInfo(BaseModel):
    isbn: int
    title: Optional[str] = None
    date: datetime.datetime = lambda: datetime.datetime.now()

@app.post("/request")
async def request_book(book: RequestBookInfo):
    return book
