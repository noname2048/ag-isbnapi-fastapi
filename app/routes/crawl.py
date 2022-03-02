from readline import insert_text
from fastapi import APIRouter, Query, BackgroundTasks
from app.nosql.conn import mongodb
import datetime

from app.task.back_crawl import single_crawl

router = APIRouter()


@router.get("/crawl")
async def simple_crwal_request(
    bg_tasks: BackgroundTasks,
    isbn: str = Query(..., title="isbn", regex=r"^[0-9]{13}$"),
):
    collection = mongodb.client["isbn"]["requests"]
    request = await collection.find_one({"isbn": isbn})

    if request:
        return {"msg": "already crwaled"}

    request = {
        "isbn": isbn,
        "status": "requested",
        "request_date": datetime.datetime.utcnow(),
        "updated_date": datetime.datetime.utcnow(),
    }

    inserted = await collection.insert_one(request)
    result = await collection.find_one(inserted.inserted_id)
    result["_id"] = str(result["_id"])
    return result


@router.get("/cral/back")
async def single_back_crawl(isbn: str = Query(..., regex=r"^[0-9]{13}$")):
    requests_coll = mongodb.client["isbn"]["requests"]
    request = await requests_coll.find_one({"isbn": isbn})

    if not request:
        return {"msg": "request not exists, call '/crawl' first"}

    books_coll = mongodb.client["isbn"]["books"]
    book = await books_coll.find_one({"isbn": isbn})
    if book:
        return book

    new_book = await single_crawl(request["_id"])
    return new_book
