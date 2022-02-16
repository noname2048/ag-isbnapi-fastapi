from fastapi import APIRouter, Request, Path, Depends
from sqlalchemy.orm import Session
from app.database.conn import postgresql_db
from app.database.sa_model import RequestRecord
from app.nosql.conn import mongodb

router = APIRouter()


@router.get("/request/isbn/{isbn}")
async def request_isbn(
    request: Request,
    isbn: Path(regex=r"\d{13}"),
    session: Session = Depends(postgresql_db.session),
):
    """isbn으로 책등록 요청을 받습니다.

    몽고 DB에서 isbn으로 검색하여 없으면 postgresql 에 등록합니다.
    :param: isbn
    """
    one = await mongodb.client.isbn.books.find_one({"isbn": isbn})
    if one:
        raise Exception("already have one")
    else:
        query = session.query(RequestRecord).filter(RequestRecord.isbn == isbn)
        if query.first():
            
