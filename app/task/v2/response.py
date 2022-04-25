from typing import List
import re
import json
import requests
from datetime import datetime, timedelta

from boto3 import resource
from boto3 import s3
from botocore.exceptions import ClientError

from app.common.config import settings
from app.odmantic import get_engine
from odmantic import AIOEngine
from app.odmantic.models import Request, Book, RequestForm
from app.utils.logger import mylogger

from app.exceptions.base import APIExceptionBase
from starlette import status

aladin_api_url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
ttbkey = settings.aladin_ttbkey
isbn13_pattern = re.compile(r"^\d{13}$")


class RequestFormResponseError(Exception):
    status_msg: str

    def __init__(self, msg):
        self.status_msg = msg
        super().__init__(msg)


def item_to_book(item) -> Book:
    kst = datetime.utcnow() + timedelta(hours=9)
    return Book(
        title=item[0]["title"],
        description=item[0]["description"],
        isbn13=item[0]["isbn13"],
        publisher=item[0]["publisher"],
        price=item[0]["priceStandard"],
        pub_date=datetime.strptime(item[0]["pubDate"], "%Y-%m-%d"),
        author=item[0]["author"],
        cover=item[0]["cover"],
        created_at=kst,
        updated_at=kst,
    )


def update_book_with_item(item, book: Book) -> Book:
    kst = datetime.utcnow() + timedelta(hours=9)
    book.title = item[0]["title"]
    book.description = item[0]["description"]
    book.isbn13 = item[0]["isbn13"]
    book.publisher = item[0]["publisher"]
    book.price = item[0]["priceStandard"]
    book.pub_date = datetime.strptime(item[0]["pubDate"], "%Y-%m-%d")
    book.author = item[0]["author"]
    book.cover = item[0]["cover"]
    book.updated_at = kst
    return book


def upload_aws(url, isbn):
    bucket = resource(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=settings.boto3_aws_access_id,
        aws_secret_access_key=settings.boto3_aws_access_key,
    ).Bucket("job-book-image")

    obj = bucket.Object(f"{isbn}.jpg")
    try:
        obj.load()
        mylogger.warn(f"image already uploaded ({isbn})")
    except ClientError as e:
        res = requests.get(url)
        img = res.raw
        obj.upload_fileobj(img)
        mylogger.debug(f"image uploaded ({isbn})")


async def process_single_request(engine: AIOEngine, request_form: RequestForm) -> Book:
    isbn13 = request_form.isbn13
    if not isbn13_pattern.match(isbn13):
        raise RequestFormResponseError("Unvalid ISBN format")

    book = await engine.find_one(Book, Book.isbn13 == request_form.isbn)
    if book and request_form.update_option == False:
        raise RequestFormResponseError("No update option but book exists")

    response = requests.post(
        aladin_api_url,
        {
            "TTBKey": ttbkey,
            "itemIdType": "isbn13",
            "ItemId": isbn13,
            "Cover": "Big",
            "output": "js",
        },
    )
    if response.status_code != 200:
        mylogger.warn("Cannot fetch with Aladin")

    try:
        text = response.text[:-1]
        item = json.loads(text, strict=False)
        item = item.get("item", None)
    except json.decoder.JSONDecodeError:
        raise RequestFormResponseError("JSON decode error")

    if not item:
        raise RequestFormResponseError("Item not found")

    try:
        if book:
            book = update_book_with_item(item, book)
        else:
            book = item_to_book(item)
    except KeyError:
        raise RequestFormResponseError("Key extract error")

    url = book.cover
    book.cover = f"{isbn13}.jpg"

    upload_aws(url, isbn13)
    book = await engine.save(book)
    return book


async def respond_single_request(obj_id: str):
    engine = get_engine()
    request_form = await engine.find_one(RequestForm, RequestForm.id == obj_id)
    if not request_form:
        mylogger.warn("Unvalid requestform id")
        return False

    try:
        book = await process_single_request(request_form)
    except RequestFormResponseError as e:
        mylogger.warn(f"{e.status_msg} ({request_form.isbn})")
        kst = datetime.utcnow() + timedelta(hours=9)
        request_form.status_msg = e.status_msg
        request_form.response_date = kst
        request_form = await engine.save(request_form)
        return False

    return True


async def respond_multiple_request(id_list: list):
    async def f(x):
        await respond_single_request(x)

    result = [1 if f(id) == True else 0 for id in id_list]
    return result
