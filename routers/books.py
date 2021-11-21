from typing import Optional
from fastapi import APIRouter
from fastapi import Query

router = APIRouter()


@router.get("/books/search", tags=["books", "search"])
async def search_isbn(title: Optional[str] = Query(), isbn: Optional[str] = Query()):
    # TODO: 몽고 DB에서 검색하기
    return {"isbn": isbn}
