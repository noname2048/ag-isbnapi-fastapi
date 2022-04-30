from typing import Optional
from fastapi import APIRouter, Query
from urllib import parse
from app.odmantic.connect import singleton_mongodb
from app.odmantic import get_engine
from app.odmantic.models import Book

router = APIRouter()


@router.get("/books")
async def books(limit: Optional[int] = Query(10, le=100)):
    """"""
    engine = singleton_mongodb.engine
    books = await engine.find(Book, {}, limit=limit)
    if books:
        return books
    return []


@router.get("/books/search/title")
async def search_by_title(q: str = Query(...)):
    engine = get_engine()
    q = parse.unquote(q)
    books = await engine.find(
        Book,
        Book.title.match(q),
    )
    if books:
        return books
    return []


@router.get("/books/search/isbn")
async def search_by_isbn(q: str = Query(..., regex=r"^\d{13}$")):
    engine = get_engine()
    books = await engine.find(Book, Book.isbn13.match(int(q)))
    if books:
        return books
    return []
