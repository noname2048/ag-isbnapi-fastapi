from sqlalchemy.orm import Session
from isbnapi.db.models import DbBook
from isbnapi.schemas import MissingBook


def create_book(db: Session, request: MissingBook):
    pass


def get_all_books(db: Session):
    return db.query(DbBook).limit(100).all()
