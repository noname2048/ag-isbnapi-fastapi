from fastapi import APIRouter
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request

router = APIRouter()


@router.get("/requests")
async def requests():
    """"""
    engine = singleton_mongodb.engine()
    requests = await engine.find(Request, {}, limit=100)
    if requests:
        return requests
    return []
