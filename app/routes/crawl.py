from readline import insert_text
from fastapi import APIRouter, Query
from app.nosql.conn import mongodb
import datetime

router = APIRouter()


@router.get("/crawl")
async def smple_crwal_request(isbn: str = Query(...)):
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
    return result
