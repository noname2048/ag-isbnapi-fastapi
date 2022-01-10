from typing import Optional, List
from fastapi import APIRouter, Query, Path, HTTPException, Body, BackgroundTasks

from app.nosql import mongo_db
from app.nosql.model import Book, Request, Response
import regex
import datetime
from app.task.aladin_api import do_request_task

from pydantic import BaseModel, Field as PyField

router = APIRouter()


class PagenationQueryParams:
    def __init__(
        self, limit: int = Query(10, ge=10, le=100), offset: int = Query(0, ge=0)
    ):
        self.limit = limit
        self.offset = offset


@router.get("")
async def books(limit: Optional[int] = Query(10, le=100)):
    ret = await mongo_db.engine.find(Book, sort=Book.pub_date.desc(), limit=limit)
    return ret


@router.get("/search", tags=["search"])
async def books_search(
    title: Optional[str] = Query(None),
    isbn13: Optional[int] = Query(None),
    limit: Optional[int] = Query(10, le=100),
):
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
    ret = await mongo_db.engine.find(Request, limit=limit)
    return ret


class ISBN13(BaseModel):
    isbn13: int

    class Config:
        schema_extra = {"example": {"isbn13": 9791188102051}}


@router.post("/requests", tags=["requests"], response_model=List[Request])
async def books_requests_accept(
    background_tasks: BackgroundTasks,
    isbn13_list: List[ISBN13] = Body(...),
):
    request_list = []
    for isbn13_obj in isbn13_list:
        isbn13 = isbn13_obj.isbn13
        if not regex.match(r"\d{13,13}", str(isbn13)):
            n = datetime.datetime.now()
            r = Request(isbn13=isbn13, request_date=n, result_code=400)
            r = await mongo_db.engine.save(r)
            request_list.append(r)
        else:
            target_book = await mongo_db.engine.find_one(
                Book, Book.isbn13.match(isbn13)
            )
            if not target_book:
                target_request = await mongo_db.engine.find_one(
                    Request, Request.isbn13.match(isbn13)
                )
                if not target_request:
                    n = datetime.datetime.now()
                    r = Request(isbn13=isbn13, request_date=n, result_code=200)
                    r = await mongo_db.engine.save(r)

                    background_tasks.add_task(do_request_task, mongo_object_id=r.id)
                    request_list.append(r)

    return request_list


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
