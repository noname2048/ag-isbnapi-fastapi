from typing import Tuple, Any
from fastapi import BackgroundTasks
import requests
from dotenv import dotenv_values
from isbnapi.web.env import get_setting
import json
from isbnapi.schemas import BookBase, BookInfoBase, BookInfoErrorBase
from datetime import date, datetime
from pathlib import Path
from sqlalchemy.orm import Session
from isbnapi.db.models import DbBook, CoverType, DbBookInfo
import shutil
from datetime import date, datetime
from isbnapi.db.database import get_db
from isbnapi.db import db_bookinfo

setting = get_setting()
ALADIN_API_ENDPOINT = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"


def get_bookinfo(isbn: str, missingbook_id: int) -> Tuple[bool, Any]:
    response = requests.post(
        url=ALADIN_API_ENDPOINT,
        data={
            "TTBKey": setting.ttbkey,
            "itemIdType": "isbn13",
            "ItemId": isbn,
            "Cover": "Big",
            "output": "js",
        },
    )

    if response.status_code != 200:
        return False, "Aladin not ok"

    text: str = response.text[:-1]
    try:
        _json = json.loads(text, strict=False)
        with open(
            Path(__file__).parent / "last_json.json", "w+", encoding="utf8"
        ) as buffer:
            json.dump(_json, buffer, ensure_ascii=False)
    except json.JSONDecodeError:
        with open(Path(__file__).parent / "last_text.txt", "w+") as buffer:
            buffer.write(text + "\n")
        return False, "Cannot parse json"

    if _json.get("errorCode", None):
        return False, _json.get("errorMessage", "Unknown aladin error")

    book = None
    try:
        target = _json["item"][0]
        _date = target["pubDate"].split("-")
        book_request = BookBase(
            isbn=target["isbn13"],
            title=target["title"],
            description=target["description"],
            cover=target["cover"],
            cover_type="absolute",
            publisher=target["publisher"],
            price=target["priceStandard"],
            pub_date=date(*map(int, _date)),
            author=target["author"],
            missingbook_id=missingbook_id,
        )
    except KeyError as e:
        return False, f"Keyerror {e.args[0]}"

    return True, book_request


def upload_image(db: Session, book: DbBook):
    if not book:
        return

    if book.cover_type == CoverType.relative:
        return

    url: str = book.cover
    response = requests.get(url=url, stream=True)

    if not response.ok:
        return

    response.raw.decode_content = True
    image = response.raw

    date_str = date.today().strftime("%y%m%d")
    filename = f"{book.isbn}_{date_str}.jpg"
    folder = f"isbnapi/bookimages/"
    with open(folder + filename, "wb+") as buffer:
        shutil.copyfileobj(image, buffer)

    book.cover = filename
    book.cover_type = CoverType.relative
    db.commit()

    now = datetime.utcnow()
    with open("isbnapi/bookimages/log.txt", "a+") as buffer:
        buffer.write(f"{now} - {book.isbn}\n")


class AladinException(Exception):
    pass


def get_bookinfo_from_aladin(isbn: str, bg):
    with open("logs.txt", "w+") as f:
        print("NOT", file=f)
    db: Session = next(get_db())
    if db.query(DbBookInfo).filter(DbBookInfo.isbn == isbn).first():
        return
    try:
        response = requests.post(
            url=ALADIN_API_ENDPOINT,
            data={
                "TTBKey": setting.ttbkey,
                "itemIdType": "isbn13",
                "ItemId": isbn,
                "Cover": "Big",
                "output": "js",
            },
        )

        if response.status_code != 200:
            raise AladinException(detail="Aladin not ok")

        text: str = response.text[:-1]
        try:
            bookjson = json.loads(text, strict=False)
        except json.JSONDecodeError:
            dir = Path(__file__).parent
            filename = dir / f"error_{isbn}.logs"
            with open(filename, "w+") as buffer:
                buffer.write(text + "\n")
            raise AladinException("Cannot parse json")

        if bookjson.get("errorCode", None):
            detail = bookjson.get("errorMessage", "Unknown aladin error")
            raise AladinException(detail=detail)

        try:
            target = bookjson["item"][0]
            bookinfobase = BookInfoBase(
                isbn=target["isbn13"],
                title=target["title"],
                description=target["description"],
                cover=target["cover"],
                cover_type="absolute",
                publisher=target["publisher"],
                price=target["priceStandard"],
                pub_date=date(*map(int, target["pubDate"].split("-"))),
                author=target["author"],
            )
        except KeyError as e:
            raise AladinException(detail=f"Keyerror {e.args[0]}")
        bookinfo = db_bookinfo.create_bookinfo(db, bookinfobase)

        bg.add_task(update_relative_bookinfo_image, isbn)

        return bookinfo

    except AladinException as e:
        error_bookinfo = BookInfoErrorBase(isbn=isbn, is_error=True, error_msg=e.detail)
        bookinfo = db_bookinfo.create_error_bookinfo(db, error_bookinfo)

        return bookinfo


def update_relative_bookinfo_image(isbn: str):
    with open("logs.txt", "w+") as f:
        print("WHAT", file=f)
    db: Session = next(get_db())
    bookinfo: DbBookInfo = db.query(DbBookInfo).filter(DbBookInfo.isbn == isbn).first()
    if bookinfo.cover_type == CoverType.relative:
        return

    response = requests.get(url=bookinfo.cover, stream=True)
    if not response.ok:
        return

    response.raw.decode_content = True
    image = response.raw

    date_str = date.today().strftime("%y%m%d")
    filename = "isbnapi/bookimages/" + f"{isbn}_{date_str}.jpg"
    with open(filename, "wb+") as buffer:
        shutil.copyfileobj(image, buffer)

    bookinfo.cover = filename
    bookinfo.cover_type = CoverType.relative
    db.commit()

    with open("isbnapi/bookimages/log.txt", "a+") as buffer:
        buffer.write(f"{datetime.utcnow()} - {isbn}")
