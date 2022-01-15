"""백그라운드 태스크가 작동하지 않는것 같습니다.
디버그를 해보니 s3 업로드에서 무한히 기다립니다. 뭐가 문제일까요?
해답을 찾아봅시다

isbn13 -> txt -> json -> db -> image -> upload
각 간격의 에러 이름:
get_res, json_serializer, db_serializer, get_image, image_upload
"""
import boto3
from app.settings import config

import aiohttp
from app.settings.base import REPO_DIR

import json

import asyncio
from typing import Dict
from app.nosql.model import Book, Response
import datetime
from app.nosql import mongo_db


async def get_text(isbn13):
    text, detail = None, None
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx",
            data={
                "TTBKey": config["ALADIN_TTB_KEY"],
                "itemIdType": "isbn13",
                "ItemId": str(isbn13),
                "Cover": "Big",
                "output": "js",
            },
        ) as response:
            if response.status != 200:
                detail = await response.text()
                return text, detail
            else:
                text = await response.text()
                return text, detail


async def get_item(text):
    data_dict, detail = None, None
    corrected_text = text[:-1]
    try:
        data_dict = json.loads(corrected_text, strict=False)
        item = data_dict["item"][0]

    except json.JSONDecodeError:
        detail = corrected_text

    except KeyError as e:
        detail = f"KeyError: {e}"

    except IndexError as e:
        detail = f"IndexError: {e}"

    return item, detail


async def get_book(item):
    book, detail = None, None
    book = Book(
        title=item["title"],
        description=item["description"],
        isbn13=item["isbn13"],
        cover=item["cover"],
        publisher=item["publisher"],
        price=item["priceStandard"],
        pub_date=datetime.datetime.strptime(item["pubDate"], "%Y-%m-%d"),
        author=item["author"],
        created_at=datetime.datetime.now(),
    )

    return book, detail


async def get_image(target_url):
    """url정보를 통해서 이미를 가져오는 함수"""
    image, detail = None, None
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            if response.status != 200:
                detail = "image fail: {response.status}"
            else:
                image = await response.read()

    return image, detail


async def get_url(image, name: str):
    """이미지 객체를 받아 S3에 저장하는 함수
    파일명을 추가 함수로 받습니다.
    """
    url, detail = None, None
    s3 = boto3.session.Session().client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=config["aws_id"],
        aws_secret_access_key=config["aws_key"],
    )

    uploaded = s3.put_object(
        Body=image,
        Bucket="job-book-image",
        Key=name,
    )
    print(uploaded)
    return url, detail


async def make_response(isbn13):
    response = Response(
        isbn13=isbn13,
        success=False,
        created_at=datetime.datetime.now(),
    )

    class MyException(Exception):
        pass

    try:
        text, detail = await get_text(isbn13)
        if not text:
            raise MyException(detail)

        item, detail = await get_item(text)
        if not item:
            raise MyException(detail)

        book, detail = await get_book(item)
        if not book:
            raise MyException(detail)

        image, detail = await get_image(book.cover)
        if not image:
            raise MyException(detail)

        url, detail = await get_url(image, f"{isbn13}.jpg")
        if not url:
            raise MyException(detail)

    except MyException as e:
        detail = e.args
        response.detail = detail

    response.success = True
    response.created_at = datetime.datetime.now()
    response = await mongo_db.engine.save(response)

    book.cover = url
    book.created_at = datetime.datetime.now()
    book = await mongo_db.engine.save(book)

    return response


if __name__ == "__main__":
    ans = asyncio.run(make_response(9791158390983))
    print(ans)
