from typing import List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from isbnapi.schemas import MissingBookBase, MissingBookFailDisplay, MissingBook
from isbnapi.db.models import DbMissingBook
from datetime import datetime
import re
from sqlalchemy.exc import IntegrityError

isbn_pattern = re.compile(r"\d{13}")


def create_missingbook(db: Session, request: MissingBookBase):
    if not isbn_pattern.match(request.isbn):
        return MissingBookFailDisplay(isbn=request.isbn, detail="Invaild ISBN")

    new_missingbook = DbMissingBook(isbn=request.isbn)
    db.add(new_missingbook)
    try:
        db.commit()
    except IntegrityError as e:
        d: str = e.orig.args[0]
        if d.startswith("UNIQUE"):
            return MissingBookFailDisplay(isbn=request.isbn, detail="Not unique key")
        raise e
    db.refresh(new_missingbook)
    return new_missingbook


def get_all_missingbooks(db: Session):
    return db.query(DbMissingBook).limit(100).all()


def get_missingbook_by_id(db: Session, id: int):
    missingbook = db.query(DbMissingBook).filter(DbMissingBook.id == id).first()
    if not missingbook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Missingbook with id {id} not found",
        )
    return missingbook
