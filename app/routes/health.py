from fastapi import APIRouter
from app.nosql.conn import mongodb

router = APIRouter()


router.get("/health/mongodb")


async def is_mongo_works():
    collection = mongodb.client["isbn"]["books"]
    document = collection.find({}, limit=1)
    return document
