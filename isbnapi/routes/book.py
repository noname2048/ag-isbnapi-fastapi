from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db.models import DbMissingBook
from isbnapi.schemas import BookDisplayExample, MissingBook, BookBase
from isbnapi.db import db_book, db_missingbook


router = APIRouter(prefix="/book", tags=["book"])

# Create book
async def create_book(request: MissingBook, db: Session = Depends(get_db)):
    missingbook = (
        db.query(DbMissingBook)
        .filter(DbMissingBook.id == request.id)
        .filter(DbMissingBook.isbn == request.isbn)
        .first()
    )
    if missingbook.error_code:
        raise HTTPException()  # aceept but nothing to do
    # aladin
    return db_book.create_book(db, request)


# Get all books
@router.get("s", response_model=BookDisplayExample)
async def get_all_books(db: Session = Depends(get_db)):
    return db_book.get_all_books()


# Get book by isbn
@router.get("/isbn/{isbn}")
async def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    return db_book.get_all_books(db, isbn)
