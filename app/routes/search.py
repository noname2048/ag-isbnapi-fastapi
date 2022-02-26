from optparse import Option
from typing import Optional
from fastapi import APIRouter, Query
from app.nosql.conn import mongodb

router = APIRouter()


@router.get("/search/title")
async def simple_title_search(
    q: str = Query(...),
    offset: Optional[int] = Query(0),
    limit: Optional[int] = Query(10),
):
    collection = mongodb.client["isbn"]["books"]
    document = collection.find({"title": q}, limit=limit)
    return document


@router.get("/search/isbn")
async def simple_isbn_search(
    q: str = Query(...),
    offset: Optional[int] = Query(0),
    limit: Optional[int] = Query(10),
):
    collection = mongodb.client["isbn"]["books"]
    document = collection.find({"isbn": q}, limit=limit)
    return document


@router.get("/depreciate")
async def search(
    isbn: Optional[str] = Query(
        None,
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        examples={
            "only_number": {"value": {"isbn": "9788966261840"}},
            "include_hippen": {"value": {"isbn": "979-11-6254-196-8"}},
        },
    ),
    title: Optional[str] = Query(
        None, title="title", description="책 검색에 사용될 제목", min_length=1
    ),
):
    """
    # 검색용 API
    query로 isbn, 혹은 title을 받아 해당하는 책의 내용을 리턴합니다.

    isbn은 -가 포함되어있어도 괜찮으며, title 이용시 좌우 공백은 제거됩니다.

    내부 DB에 있는 책 정보를 검색하여 리턴합니다.

    **isbn과 title 모두 있으면 isbn을 사용합니다.**
    """
    if isbn is not None and title is not None:
        title = None

    if isbn is not None:
        # TODO: 몽고DB 접근후 결과 반환
        return {"data": ""}

    else:
        # TODO: 몽고DB 접근후 결과 반환
        return {"data": ""}
