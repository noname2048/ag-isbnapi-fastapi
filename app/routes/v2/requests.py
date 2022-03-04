from fastapi import APIRouter
from app.nosql.conn import mongodb

router = APIRouter()


@router.get("/requests")
async def requests():
    requests_coll = mongodb.client["isbn"]["requests"]
    cursor = requests_coll.find({})
    cursor.limit(20)
    target = cursor.to_list(length=20)
    return target
