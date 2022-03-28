from fastapi import APIRouter
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request, Book
from app.task.crawl import f1

router = APIRouter()


@router.get("/responses/make")
async def check_request_manually():
    """
    몽고DB에서 requested, 와 need update 를 확인
    해당 객체의 book 만들고 결과 반환
    최근 것 딱 한개만 만든다.
    """
    engine = singleton_mongodb.engine
    request = await engine.find_one(
        Request, Request.status.in_(["requested", "need update"])
    )
    if not request:
        return {"msg": "모두 업데이트 되었습니다."}
    book = await f1(request.id)
    request.status = "registered"
    request = await engine.save(request)
    return {"book": book, "request": request}
