from typing import List
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    BackgroundTasks,
    Path,
)
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db.models import DbBook, DbMissingBook, DbBookInfo, DbTempBook
from isbnapi.schemas import BookDisplayExample, BookInfoDisplay, MissingBook, BookBase
from isbnapi.db import db_book, db_missingbook, db_tempbook
from isbnapi.web import aladin
import re
from isbnapi.schemas import TempBookDisplay, TempBookBase
from typing import Union
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter(prefix="/book", tags=["book"])


isbn_pattern = re.compile(r"\d{13}")


@router.get("s/{isbn}", response_model=BookInfoDisplay)
async def get_book_by_isbn(
    response: Response,
    bg_tasks: BackgroundTasks,
    isbn: str = Path(..., regex=r"^[0-9]{13}"),
    db: Session = Depends(get_db),
):
    book: DbBookInfo = db.query(DbBookInfo).filter(DbBookInfo.isbn == isbn).first()
    if book:
        return book

    tempbook = db.query(DbTempBook).filter(DbTempBook.isbn == isbn).first()
    if not tempbook:
        tempbook = db_tempbook.create(db, TempBookBase(isbn=isbn))
    tempbook = TempBookDisplay(
        id=tempbook.id, isbn=tempbook.isbn, timestamp=tempbook.timestamp
    )

    bg_tasks.add_task(aladin.get_bookinfo_from_aladin, isbn, bg_tasks)
    response = JSONResponse(
        content=jsonable_encoder(tempbook), status_code=status.HTTP_202_ACCEPTED
    )
    return response


@router.get("s", response_model=List[BookDisplayExample])
async def get_all_books(db: Session = Depends(get_db)):
    return db_book.get_all_books(db)


@router.post(
    "",
    responses={
        200: {"model": BookDisplayExample},
        202: {
            "content": {
                "application/json": {"example": {"detail": "detail error description"}}
            }
        },
        400: {
            "content": {
                "application/json": {"example": {"detail": "Check id and isbn"}}
            }
        },
    },
)
async def create_book(
    bg_task: BackgroundTasks,
    request: MissingBook,
    db: Session = Depends(get_db),
):
    # check missing book
    missingbook: DbMissingBook = (
        db.query(DbMissingBook)
        .filter(DbMissingBook.id == request.id)
        .filter(DbMissingBook.isbn == request.isbn)
        .first()
    )

    if not missingbook:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Check id and isbn",
        )

    book = db.query(DbBook).filter(DbBook.isbn == request.isbn).first()
    if book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="book already exists",
        )

    condition, result = aladin.get_bookinfo(request.isbn, request.id)
    if not condition:
        detail: str = result
        missingbook.error_message = detail
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=result,
        )
    missingbook.error_message = ""
    db.commit()

    bookbase: BookBase = result
    book = db_book.create_book(db, bookbase)
    bg_task.add_task(aladin.upload_image, db, book)
    return book
