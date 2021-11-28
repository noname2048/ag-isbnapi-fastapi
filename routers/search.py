from typing import Optional
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api/v1/search",
    tags=["search"],
    responses={
        200: {"description": "Ok"},
        400: {"description": "Bad Request"},
        404: {"description": "Not found"},
    },
)


@router.get("/")
async def search(
    isbn: Optional[str] = Query(
        None,
        title="isbn(13자리)",
        description="책 검색에 사용될 13자리 isbn",
        min_length=13,
        regex="^[0-9-]{13,}",
        examples={
            "only_number": "9788966261840",
            "include_hippen": "979-11-6254-196-8",
        },
    ),
    title: Optional[str] = Query(
        None, title="title", description="책 검색에 사용될 제목", min_length=1
    ),
):
    """
    검색용 API, isbn 혹은 title을 필요로 합니다.
    isbn은 -가 포함되어있어도 괜찮으며, title 이용시 좌우 공백은 제거됩니다.

    내부 DB에 있는 책 정보를 검색하여 리턴합니다.
    """
    if isbn is not None and title is not None:
        title = None

    if isbn is not None:
        # TODO: 몽고DB 접근후 결과 반환
        return {"data": ""}

    else:
        # TODO: 몽고DB 접근후 결과 반환
        return {"data": ""}
