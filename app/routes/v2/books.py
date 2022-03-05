from typing import Optional
from fastapi import APIRouter, Query

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Book

router = APIRouter()


@router.get("/books")
async def books(limit: Optional[int] = Query(10, le=100)):
    """"""
    engine = singleton_mongodb.engine()
    books = await engine.find(Book, {}, limit=limit)
    if books:
        return books
    return []
