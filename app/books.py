from typing import Optional, List, Final
from fastapi import APIRouter, Query, Path, HTTPException, Body, BackgroundTasks

from app.nosql import mongo_db
from app.nosql.model import Book, Request, Response
import regex
import datetime
from app.task.aladin_api import do_request_task

from pydantic import BaseModel, Field as PyField

router = APIRouter()


@router.get("")
async def books(limit: Optional[int] = Query(10, le=100)):
    """사용된다고 가정하지 않는 기본 / 루트

    검색창에 아무것도 입력하지 않았을 때 최근 출판된 10개의 책을 json 리턴합니다.
    """
    ret = await mongo_db.engine.find(Book, sort=Book.pub_date.desc(), limit=limit)
    return ret


@router.get("/search", tags=["search"])
async def books_search(
    title: Optional[str] = Query(None),
    isbn13: Optional[int] = Query(None),
    limit: Optional[int] = Query(10, le=100),
):
    """기본 검색 함수, title과 isbn13(우선)을 지원합니다.

    두 개 모두 입력되지 않았다면 최근 출판된 10개의 책을 json 리턴합니다.
    """
    if isbn13:
        ret = await mongo_db.engine.find(Book, Book.isbn13.match(isbn13), limit=limit)
        return ret
    elif title:
        ret = await mongo_db.engine.find(Book, Book.title.match(title), limit=limit)
    else:
        ret = await mongo_db.engine.find(Book, Book.pub_date.desc(), limit=limit)

    return ret


@router.get("/requests", tags=["requests"], response_model=List[Request])
async def books_reqeusts_list(
    title: Optional[str] = Query(None),
    isbn13: Optional[int] = Query(None),
    limit: Optional[int] = Query(10, le=100),
):
    """최근의 리퀘스트를 보여주는 함수, title과 isbn13(우선)을 지원합니다.

    아무것도 입력되지 않았다면 최근 만들어진 Request 10개를 보여줍니다.
    """
    if isbn13:
        ret = await mongo_db.engine.find(
            Request, Request.isbn13.match(isbn13), limit=limit
        )
        return ret
    elif title:
        ret = await mongo_db.engine.find(
            Request, Request.title.match(title), limit=limit
        )
    else:
        ret = await mongo_db.engine.find(
            Request, Request.created_at.desc(), limit=limit
        )

    ret = await mongo_db.engine.find(Request, limit=limit)
    return ret


class ISBN13(BaseModel):
    isbn13: int

    class Config:
        schema_extra = {"example": {"isbn13": 9791188102051}}


ISBN_MIN = 10 ** 12
ISBN_MAX = 10 ** 13


def verify_isbn(isbn: int):
    return isbn < ISBN_MIN and isbn > ISBN_MAX


@router.post("/requests", tags=["requests"], response_model=List[Request])
async def books_requests_accept(
    background_tasks: BackgroundTasks,
    list_of_isbn13_object: List[ISBN13] = Body(...),
):
    """request를 생성을 post로 요청받는 함수

    [{ "isbn": ~(number) }] 의 형태를 지원받습니다.
    결과로 생성된 [{ requst_id: ~ , ... }] 을 돌려줍니다.

    이미 있는 request는 무시합니다.

    생성된 request는 자동으로 background task를 작동시킵니다.
    """
    created_requests: List[Request] = []
    for item in list_of_isbn13_object:
        isbn13 = item.isbn13

        # 유효한 isbn13 인지
        if verify_isbn is False:
            unsaved_request = Request(
                isbn13=isbn13, request_date=datetime.datetime.now(), result_code=400
            )
            saved_request = await mongo_db.engine.save(unsaved_request)
            created_requests.append(saved_request)
        else:
            book_existance = await mongo_db.engine.find_one(
                Book, Book.isbn13.match(isbn13)
            )
            request_existance = await mongo_db.engine.find_one(
                Request, Request.isbn13.match(isbn13)
            )
            if not book_existance and not request_existance:
                unsaved_request = Request(
                    isbn13=isbn13,
                    created_at=datetime.datetime.now(),
                    status_code=200,
                )
                saved_request = await mongo_db.engine.save(unsaved_request)

                background_tasks.add_task(
                    do_request_task, mongo_object_id=saved_request.id
                )
                created_requests.append(saved_request.id)

    return created_requests


@router.get("/reqeusts/{id}", tags=["requests"])
async def books_requests_detail(id: str = Path(...)):
    ret = await mongo_db.engine.find_one(Request, Request.id.match(id))
    if ret:
        return ret
    else:
        raise HTTPException(status_code=404, detail="No Requests found, have id({id})")


@router.get("/requests/search", tags=["reqeusts"])
async def books_requests_search(
    title: Optional[str] = Query(None),
    isbn13: Optional[int] = Query(None),
    limit: Optional[int] = Query(10, le=100),
):
    if isbn13:
        ret = await mongo_db.engine.find(
            Request, Request.isbn13.match(isbn13), limit=limit
        )
        return ret
    elif title:
        ret = await mongo_db.engine.find(
            Request, Request.title.match(title), limit=limit
        )
    else:
        ret = await mongo_db.engine.find(Request, Request.pub_date.desc(), limit=limit)

    return ret


@router.get("/requests/{id}/response", tags=["reqeusts"])
async def books_reqeusts_response(id: str = Path(...)):
    request = await mongo_db.engine.find_one(Request, Request.id.match(id))
    if request:
        response = await mongo_db.engine.find_one(
            Response, Response.id.match(request.response_id)
        )
        if response:
            return response
        else:
            raise HTTPException(
                status_code=404,
                detail="No Response found, have id({requests.response_id})",
            )
    else:
        raise HTTPException(status_code=404, detail="No Requests found, have id({id})")


@router.get("/responses", tags=["responses"])
async def books_response_list(limit: Optional[int] = Query(10, le=100)):
    ret = await mongo_db.engine.find(Response, Response.date.desc(), limit=limit)
    return ret


@router.get("/responses/{id}", tags=["responses"])
async def books_response_detail(id: str = Path(...)):
    response = await mongo_db.engine.find_one(Response, Response.id.match(id))
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No Response Found, have id({id})")


@router.get("/responses/{id}/request", tags=["responses"])
async def books_responses_request(id: str = Path(...)):
    response = await mongo_db.engine.find_one(Response, Response.id.match(id))
    if response:
        request = await mongo_db.engine.find_one(
            Request, Request.id.match(response.request_id)
        )
        if request:
            return request
        else:
            raise HTTPException(status_code=500, detail="Somethings go wrong.")
    else:
        raise HTTPException(status_code=404, detail="No Response Found, have id({id})")
