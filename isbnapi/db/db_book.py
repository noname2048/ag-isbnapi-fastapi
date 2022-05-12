from sqlalchemy.orm import Session
from isbnapi.db.models import DbBook
from isbnapi.schemas import MissingBook, BookBase
from fastapi import HTTPException, status


def create_book(db: Session, request: BookBase):
    new_book = DbBook(
        isbn=request.isbn,
        title=request.isbn,
        description=request.isbn,
        cover=request.cover,
        cover_type=request.cover_type,
        pulisher=request.publisher,
        price=request.price,
        pub_date=request.pub_date,
        author=request.author,
        missingbook_id=request.missingbook_id,
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


def get_all_books(db: Session):
    return db.query(DbBook).limit(100).all()


def get_book_by_isbn(db: Session, isbn: str):
    book = db.query(DbBook).filter(DbBook.isbn == isbn).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with isbn {isbn} not found",
        )
    return book
