"""백그라운드 태스크가 작동하지 않는것 같습니다.
디버그를 해보니 s3 업로드에서 무한히 기다립니다. 뭐가 문제일까요?
해답을 찾아봅시다
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


async def upload_to_s3(image, isbn13: int):
    """이미지 객체를 받아 S3에 저장하는 함수"""
    s3_handler = boto3.resource(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=config["aws_id"],
        aws_secret_access_key=config["aws_key"],
    )
    # bucker_handler = s3_handler.Bucket("job-book-image")
    # object_handler = bucker_handler.Object(f"{isbn13}.jpg")
    # uploaded = await object_handler.upload_fileobj(image)
    uploaded = s3_handler.put_object(
        Body=image,
        Bucket="job-book-image",
        Key=f"{isbn13}.jpg",
    )

    return uploaded


async def new_upload_to_s3(image, isbn13: int):
    """이미지 객체를 받아 S3에 저장하는 함수"""
    s3 = boto3.session.Session().client(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=config["aws_id"],
        aws_secret_access_key=config["aws_key"],
    )

    uploaded = s3.put_object(
        Body=image,
        Bucket="job-book-image",
        Key=f"{isbn13}.jpg",
    )

    return uploaded


async def get_image(target_url):
    """url정보를 통해서 이미를 가져오는 함수
    디버깅을 위해 저장합니다.
    """
    image, detail = None, None
    async with aiohttp.ClientSession() as session:
        async with session.get(target_url) as response:
            if response.status != 200:
                detail = "image fail: {response.status}"
            else:
                image = await response.read()

    return image, detail


async def get_image_url(isbn13):
    """알라딘 API로부터 이미지 url을 가져옵니다."""
    image_url = None
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
            if response.status == 200:
                text = await response.text()
                corrected_text = text[:-1]
                try:
                    data_dict = json.loads(corrected_text, strict=False)

                    try:
                        item = data_dict["item"]
                        image_url = item[0]["cover"]
                    except KeyError as e:
                        print("error", e)

                except json.JSONDecodeError:
                    with open(REPO_DIR / "tmp" / "test.txt", "w") as f:
                        f.write(corrected_text)
            else:
                pass

    return image_url


async def get_item_from_isbn(isbn13):
    """알라딘에서 isbn정보를 통해 item 객체를 가지고 옵니다
    성공할 경우 item 객체를 리턴합니다.

    1. 200 코드를 응답받지 못한경우, detail에 상태코드와 사유를 적습니다. (에러시나리오1)
    2. json 과정에서 에러가 발생한경우 json으로 변환될 예정이었던 txt를 detail에 기록합니다. (에러시나리오2)
    """
    item, detail = None, None
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
                text = await response.text()
                detail = {"status_code": response.status, "data": text}
                return item, detail

            else:
                text = await response.text()
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


async def item_to_db(item: Dict):
    """item 항목을 받아옵니다"""
    book = None
    book = Book(
        title=item["title"],
        description=item["description"],
        isbn13=item["isbn13"],
        cover="",
        publisher=item["publisher"],
        price=item["priceStandard"],
        pub_date=datetime.datetime.strptime(item["pubDate"], "%Y-%m-%d"),
        author=item["author"],
    )
    image, detail = get_image(item["cover"])
    if not image:
        response = Response(isbn13=item["isbn13"])
    uploaded = new_upload_to_s3(image, item["isbn13"])
    book = await mongo_db.engine.save(book)


if __name__ == "__main__":
    ans = asyncio.run(get_image_url(9791188102051))
    ans = asyncio.run(get_image(ans))
    ans = asyncio.run(new_upload_to_s3(ans, 9791188102051))
    print(ans)
