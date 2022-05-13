from sqlalchemy.orm import Session
from isbnapi.db.models import DbBook, CoverType
import requests
import boto3


def absolute_to_relative(db: Session, book_id: int):
    book: DbBook = db.query(DbBook).filter(DbBook.id == book_id).first()
    if not book:
        return

    if book.cover_type == CoverType.relative:
        return

    url: str = book.cover
    response = requests.get(url=url)

    if not response.ok == 200:
        return

    image = response.raw

    s3 = boto3.client("s3")
    s3.upload_fileobj(image, "job-book-image", f"{book.isbn}.jpg")
