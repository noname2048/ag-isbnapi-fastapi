from fastapi import APIRouter, BackgroundTasks
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request, Book
from app.task.crawl import f1, f2

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


@router.get("/responses/make/many")
async def check_request_many(background_task: BackgroundTasks):
    """
    여러개를 동시에 만들자.
    대신, 이 일은 오래 걸릴 수 있으므로, 백그라운드 작업으로 연계 해야한다.
    """
    engine = singleton_mongodb.engine
    requests = await engine.find(
        Request,
        Request.status.in_(["requested", "need update"]),
        limit=50,
    )
    if not requests:
        return {"msg": "모두 업데이트 되었습니다."}
    isbns = [req.isbn for req in requests]
    background_task.add_task(f2, requests=requests)
    return {"isbns": isbns, "msg": "대기열에 추가되었습니다."}


@router.get("/responses")
async def list_responses():
    engine = singleton_mongodb.engine
    books = await engine.find(Book, sort=Book.updated_at.desc())
    if not books:
        return []
    return books
