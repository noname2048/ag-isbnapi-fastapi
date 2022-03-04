from typing import Optional
from fastapi import APIRouter, Query
from app.nosql.conn import mongodb

router = APIRouter()


@router.get("")
async def books(limit: Optional[int] = Query(10, le=100)):
    """사용된다고 가정하지 않는 기본 / 루트

    검색창에 아무것도 입력하지 않았을 때 최근 출판된 10개의 책을 json 리턴합니다.
    """
    books_coll = mongodb.client["isbn"]["books"]
    cursor = books_coll.find({})
    cursor.limit(10)
    target = await cursor.to_list(length=10)
    return target
