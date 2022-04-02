from typing import Optional
from fastapi import APIRouter, Body, BackgroundTasks

# import logging
# from app.main import mylogger
from app.utils.logger import mylogger
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request as RE, Book
import logging
from pydantic import BaseModel

from odmantic.exceptions import DocumentNotFoundError

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn: str = Body("")):
    return {"isbn": isbn}


class Request(BaseModel):
    isbn: str
    update: Optional[str]


@router.post("/test/echo")
async def echo_text(isbn: Request):
    mylogger.info(f"+{isbn}+")
    return {"isbn": isbn}


@router.get("/test/db/clean")
async def clean_db(background_task: BackgroundTasks):
    background_task.add_task(bt_clean_db)

    return {"msg": "start clean"}


async def bt_clean_db():
    mylogger.warn("start background: clean_db")
    engine = singleton_mongodb.engine
    mylogger.info("clean_db: start delete requests")
    await k1(RE)
    mylogger.info("clean_db: start delete books")
    await k1(Book)
    mylogger.warn("delete done.")


async def k1(model: BaseModel):
    engine = singleton_mongodb.engine
    mylogger.info("A@")
    instances = await engine.find(model)  # 여기를 지나가지 못한다.
    """
    내부에 이상한 선언을 먼저 했었는데,

    (이 파일의 앞쪽내용)
    class Request(BaseModel):
        isbn: str
        update: Optional[str]

    아무에러도 출력하지 않은채,
    진행되지 않고 끝났다
    odmantic을 사용하기 어려운 이유가 될지도.
    """
    max_roll = 20
    roll_cnt = 0
    mylogger.info("B@")
    try:
        while instances:
            for instance in instances:
                await engine.delete(instance)
            instances = await engine.find(model)
            if roll_cnt >= max_roll:
                break
            else:
                roll_cnt += 1
                mylogger.info("c@")
    except DocumentNotFoundError as e:
        mylogger.warn("error: k1")
