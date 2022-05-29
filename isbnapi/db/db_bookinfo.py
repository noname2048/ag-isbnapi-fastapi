from sqlalchemy.orm import Session
from isbnapi.db.models import DbBookInfo
from isbnapi.schemas import BookInfoBase, BookInfoErrorBase
from fastapi import HTTPException, status


def create_bookinfo(db: Session, request: BookInfoBase):
    new_bookinfo = DbBookInfo(
        isbn=request.isbn,
        title=request.title,
        description=request.description,
        cover=request.cover,
        cover_type=request.cover_type,
        publisher=request.publisher,
        price=request.price,
        pub_date=request.pub_date,
        author=request.author,
    )
    db.add(new_bookinfo)
    db.commit()
    db.refresh(new_bookinfo)
    return new_bookinfo


def create_error_bookinfo(db: Session, request: BookInfoErrorBase):
    error_bookinfo = DbBookInfo(
        isbn=request.isbn,
        is_error=True,
        error_msg=request.error_msg,
    )
    db.add(error_bookinfo)
    db.commit()
    db.refresh(error_bookinfo)
    return error_bookinfo
