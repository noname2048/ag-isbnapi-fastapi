"""백그라운드 태스크가 작동하지 않는것 같습니다.
디버그를 해보니 s3 업로드에서 무한히 기다립니다. 뭐가 문제일까요?
해답을 찾아봅시다

isbn13 -> txt -> json -> db -> image -> upload
각 간격의 에러 이름:
get_res, json_serializer, db_serializer, get_image, image_upload
"""
import asyncio
from datetime import datetime
import json
from re import I
from typing import Dict
from urllib import request

import aiohttp
import boto3

from app.settings import config
from app.settings.base import REPO_DIR
from app.nosql.odmantic import mongo_db
from app.nosql.odmantic.model import Request, Response, Book
from app.nosql.odmantic.util import clear_all


class MyException(Exception):
    """aladin_to_s3 에서 Response를 만들 때, 에러처리를 위한 예외"""

    pass


async def get_text(isbn13):
    text = None
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
                return text


async def get_item(text):
    data_dict = None
    corrected_text = text[:-1]
    try:
        data_dict = json.loads(corrected_text, strict=False)
        item = data_dict["item"][0]

    except json.JSONDecodeError:
        detail = corrected_text
        raise MyException(detail)

    except KeyError as e:
        detail = f"KeyError: {e}"
        raise MyException(detail)

    except IndexError as e:
        detail = f"IndexError: {e}"
        raise MyException(detail)

    return item


async def get_book(item) -> dict:
    book = None
    try:
        book = {
            "title": item["title"],
            "description": item["description"],
            "isbn13": item["isbn13"],
            "cover": item["cover"],
            "publisher": item["publisher"],
            "price": item["priceStandard"],
            "pub_date": datetime.strptime(item["pubDate"], "%Y-%m-%d"),
            "author": item["author"],
            "created_at": datetime.now(),
        }
    except KeyError as e:
        raise MyException(get_book.__name__, f"{get_book.__name__}에서 KeyError {e} 발생")

    return book


async def get_image(target_url):
    """url정보를 통해서 이미를 가져오는 함수"""
    image = None
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            if response.status != 200:
                detail = "image fail: {response.status}"
            else:
                image = await response.read()

    return image


async def get_url(image, name: str, save=False):
    """이미지 객체를 받아 S3에 저장하는 함수
    파일명을 추가 함수로 받습니다.
    """
    url = None

    if save:
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

        if uploaded:
            print(uploaded["ResponseMetadata"]["HTTPStatusCode"])

    url = name
    return url


async def make_response(request: Request):
    isbn13 = request.isbn13
    response = {
        "isbn13": isbn13,
        "success": False,
        "created_at": datetime.now(),
        "request_id": request.id,
    }

    try:
        text = await get_text(isbn13)
        item = await get_item(text)
        book = await get_book(item)
        image = await get_image(book["cover"])
        url = await get_url(image, f"{isbn13}.jpg")

    except MyException as e:
        detail = e.args
        response["detail"] = detail
        response["created_at"] = datetime.now()
        response = Response(**response)
        response = await mongo_db.engine.save(response)

        request.response_id = response.id
        request = await mongo_db.engine.save(request)

        return response

    response["success"] = True
    response["created_at"] = datetime.now()
    response = Response(**response)
    response = await mongo_db.engine.save(response)

    request.response_id = response.id
    request = await mongo_db.engine.save(request)

    book["cover"] = url
    book["response_id"] = response.id
    book["created_at"] = datetime.now()
    book = Book(**book)
    book = await mongo_db.engine.save(book)

    return response


async def main():
    # mongo_db.connect()
    # # await clear_all()
    # isbn13 = 9791158390983
    # request = Request(isbn13=isbn13, created_at=datetime.now())
    # await mongo_db.engine.save(request)
    # response = await make_response(request)
    # mongo_db.disconnect()
    pass


if __name__ == "__main__":
    asyncio.run(main())
