from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db.models import DbMissingBook
from isbnapi.schemas import BookDisplayExample, MissingBook, BookBase
from isbnapi.db import db_book, db_missingbook
from isbnapi.web import aladin
import re

router = APIRouter(prefix="/book", tags=["book"])

# Create book by missingbook
@router.post("")
async def create_book(request: MissingBook, db: Session = Depends(get_db)):
    # check missing book
    missingbook = (
        db.query(DbMissingBook)
        .filter(DbMissingBook.id == request.id)
        .filter(DbMissingBook.isbn == request.isbn)
        .first()
    )

    if not missingbook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Check id and isbn",
        )

    condition, result = aladin.get_bookinfo(request.isbn, request.id)
    if not condition:
        detail: str = result
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result,
        )
    bookbase: BookBase = result
    book = db_book.create_book(db, bookbase)
    return book


# Get all books
@router.get("s", response_model=List[BookDisplayExample])
async def get_all_books(db: Session = Depends(get_db)):
    return db_book.get_all_books(db)


isbn_pattern = re.compile(r"\d{13}")

# Get book by isbn
@router.get("/isbn/{isbn}")
async def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    if not isbn_pattern.match(isbn):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invaild ISBN",
        )
    return db_book.get_book_by_isbn(db, isbn)
