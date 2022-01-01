from typing import Optional
from fastapi import APIRouter, Query, Path, HTTPException

from app.nosql import mongo_db
from app.nosql.model import Book, Request, Response

router = APIRouter()


@router.get("")
async def books(limit: Optional[int] = Query(10, le=100)):
    ret = await mongo_db.engine.find(Book, sort=Book.pub_date.desc(), limit=limit)
    return ret


@router.get("/search")
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


@router.get("/requests")
async def books_reqeusts_list(
    title: Optional[str] = Query(None),
    isbn13: Optional[int] = Query(None),
    limit: Optional[int] = Query(10, le=100),
):
    pass


@router.get("/reqeusts/{id}")
async def books_requests_detail(id: str = Path(...)):
    ret = await mongo_db.engine.find_one(Request, Request.id.match(id))
    if ret:
        return ret
    else:
        raise HTTPException(status_code=404, detail="No Requests found, have id({id})")


@router.get("/requests/search")
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


@router.get("/requests/{id}/response")
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


@router.get("/responses")
async def books_response_list(limit: Optional[int] = Query(10, le=100)):
    ret = await mongo_db.engine.find(Response, Response.date.desc(), limit=limit)
    return ret


@router.get("/responses/{id}")
async def books_response_detail(id: str = Path(...)):
    response = await mongo_db.engine.find_one(Response, Response.id.match(id))
    if response:
        return response
    else:
        raise HTTPException(status_code=404, detail="No Response Found, have id({id})")


@router.get("/responses/{id}/request")
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
