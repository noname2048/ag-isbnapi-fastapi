from datetime import datetime
from fastapi import APIRouter, Body
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request

router = APIRouter()


@router.get("/requests")
async def list_requests():
    """"""
    engine = singleton_mongodb.engine
    requests = await engine.find(Request, {}, limit=100)
    if requests:
        return requests
    return []


@router.post("/requests")
async def make_request(
    isbn: str = Body(..., regex=r"^\d{13}$"), update: bool = Body(False)
):
    """"""
    engine = singleton_mongodb.engine
    request = await engine.find(Request, {"isbn": isbn})
    if request and update:
        request.status = "need update"
        await engine.save(request)
        return request

    if request:
        raise Exception("already requested")

    now = datetime.utcnow()
    new_request = Request(isbn=isbn, created_at=now, updated_at=now, status="requested")
    request = await engine.save(Request)
    return request
