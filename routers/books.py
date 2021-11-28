from typing import Optional
from fastapi import APIRouter
from fastapi import Query

router = APIRouter(
    prefix="/api/v1/books",
    tags=["books"],
    responses={
        200: {"description": "Ok"},
        400: {"description": "Bad Request"},
        404: {"description": "Not found"},
    },
)


@router.get("/recent", tags=["books", "search"])
async def recent(
    limit: int = Query(
        10, title="limit", description="API가 한번당 리턴할 책의 수", ge=1, le=100
    ),
    offset: int = Query(
        0, title="offset", description="최근 등록된 책의 목록부터 등록된 offset", ge=0
    ),
):
    """
    최근에 외부 API를 이용하여 신규 등록된 책의 목록을 반환합니다.
    최대 100개까지 한번에 요청할 수 있으며, offset을 이용하여 페이지 구성을 할 수 있습니다.
    """
    return {"data": ""}
