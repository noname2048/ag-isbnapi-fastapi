from readline import insert_text
from fastapi import APIRouter, Query, BackgroundTasks
from app.nosql.conn import mongodb
import datetime

router = APIRouter()


@router.get("/crawl")
async def smple_crwal_request(
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
