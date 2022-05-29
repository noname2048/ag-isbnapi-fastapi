from sqlalchemy.orm import Session
from isbnapi.db.models import DbTempBook
from isbnapi.schemas import TempBookBase


def create(db: Session, request: TempBookBase):
    new_tempbook = DbTempBook(
        isbn=request.isbn,
    )
    db.add(new_tempbook)
    db.commit()

    return new_tempbook
