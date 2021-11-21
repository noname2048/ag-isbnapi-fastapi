from fastapi import APIRouter
from fastapi import Path

router = APIRouter()


@router.get("/isbn/search/{isbn}", tags=["isbn", "search"])
async def search_isbn(
    isbn: str = Path(
        ...,
    )
):
    #  TODO: 몽고DB에서 isbn 검색하기
    return {"isbn": isbn}
