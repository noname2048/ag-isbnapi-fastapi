from typing import Optional, List
from fastapi import APIRouter, Query, Body, Depends, BackgroundTasks

from pydantic import BaseModel, Field
import datetime

from app.dependencies.request import BookRequestCreate, BookResponseCreate
from app.db.odmantic_core import mongo_db
from app.db.odmantic_core.book import Book
from app.db.odmantic_core.request import Request

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine, query

from app.task.aladin_api import do_request_task

engine = AIOEngine(motor_client=mongo_db.client, database="isbn")

from app.nosql.conn import mongodb

router = APIRouter()


@router.get("/request")
async def simple_isbn_request(isbn: Query(...)):
    collection = mongodb.client["isbn"]["books"]
    document = await collection.find_one({"isbn": isbn})
    if document:
        raise Exception("request target already exists")

    return {"isbn": isbn}


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


@router.get("/")
async def show_recent_request(limit: int = Query(10, title="limit", example=10)):
    request_list = await mongo_db.engine.find(
        Request, {}, sort=Request.request_date.desc(), limit=limit
    )
    return {"recent-10items": request_list}


@router.post("/")
async def request(
    background_tasks: BackgroundTasks,
    book: BookRequestCreate = Body(
        ...,
        title="book",
        description="요청 하는 책의 필요 데이터",
        examples={
            "only_number": {"value": {"isbn": "9788966261840"}},
            "include_hippen": {"value": {"isbn": "979-11-6254-196-8"}},
        },
    ),
):
    """
    외부 API를 이용하여(하루 5천회 사용가능) 내부 DB에 결과값을 저장합니다.
    json body를 통해 식별합니다.

    1. 먼저 내부 DB 확인 -> 있으면 return
    2. 이미 요청된 request 있나 확인 -> 있으면 return
    3. 1, 2가 없다는 가정하에 작업진행
    """
    isbn13 = str(book.isbn)
    if len(isbn13) != 13:
        # TODO: validation
        return {"message": "isbn is wrong, check again"}

    book_object = await engine.find_one(Book, Book.isbn13 == isbn13)
    if book_object:
        return {"message": "request already in db"}
    else:
        request_object = await mongo_db.engine.find_one(
            Request, (Request.isbn13 == int(book.isbn)) & (Request.response_code == 200)
        )

        if request_object:
            return {"message": "wait for moment. other request is in progress"}
        else:
            request = Request(
                isbn13=isbn13, request_date=datetime.datetime.now(), response_code=200
            )
            request_object = await mongo_db.engine.save(request)
            background_tasks.add_task(do_request_task, request_object.id)
    return {"request": request}


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
