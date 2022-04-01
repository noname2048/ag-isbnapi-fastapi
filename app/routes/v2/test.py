from typing import Optional
from fastapi import APIRouter, Body, BackgroundTasks

# import logging
# from app.main import mylogger
from app.utils.logger import mylogger
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request, Book
import logging
from pydantic import BaseModel

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn: str = Body("")):
    return {"isbn": isbn}


class Request(BaseModel):
    isbn: str
    update: Optional[str]


@router.post("/test/echo")
async def echo_text(isbn: Request):
    mylogger.info(f"+{isbn}+")
    return {"isbn": isbn}


@router.get("/test/db/clean")
async def clean_db(background_task: BackgroundTasks):
    background_task.add_task(delete_all)

    return {"msg": "start clean"}


async def delete_all():
    engine = singleton_mongodb.engine
    requests = await engine.find(Request, {})
    books = await engine.find(Book, {})
    for request in requests:
        await engine.delete(request)
    for book in books:
        await engine.delete(book)
    mylogger.warn("delete done.")
