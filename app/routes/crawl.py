from fastapi import APIRouter, Query
from app.nosql.conn import mongodb
import datetime

router = APIRouter()


@router.get("/crawl/")
async def smple_crwal_request(isbn: Query(...)):
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
    result = await collection.insert_one(request)
    result["_id"] = result["_id"].toString()
    return result
