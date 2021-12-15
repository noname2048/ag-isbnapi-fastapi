import aiohttp
from app.settings.base import config
import json
from app.db.odmantic_core import mongo_db
from app.db.odmantic_core.request import Request
from app.db.odmantic_core.book import Book
import datetime

ALADIN_API_URL = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
TTB_KEY = config["ALADIN_TTB_KEY"]


async def fetch(session: aiohttp.ClientSession, isbn13: int):
    data = {
        "TTBKey": TTB_KEY,
        "itemIdType": "isbn13",
        "ItemId": str(isbn13),
        "Cover": "Big",
        "output": "js",
    }
    async with session.post(ALADIN_API_URL, data=data) as response:
        status_code = response.status
        if status_code == 200:
            temp = await response.text[:-1]
            response = json.loads(temp, strict=False)
            image_url = response.get("image")


async def do_request_task(mongo_object_id: str):
    """isbn13 param를 받고나서 동작하는 백그라운드 함수

    몽고 db에 Request를 작성하고, 그 objectid를 넘겨받아 책을 검색합니다.
    Request에 처리 결과를 적어놓습니다.
    """
    request_object: Request = await mongo_db.engine.find_one(
        Request, Request.id == mongo_object_id
    )
    if request_object:
        isbn13 = request_object.isbn13

        async with aiohttp.ClientSession() as session:
            async with session.post(
                ALADIN_API_URL,
                data={
                    "TTBKey": TTB_KEY,
                    "itemIdType": "isbn13",
                    "ItemId": str(isbn13),
                    "Cover": "Big",
                    "output": "js",
                },
            ) as response:
                if response.status == 200:
                    text = await response.text()

        if text:
            result = json.loads(text[:-1], strict=False)
            item = result.get("item", None)

            if item:
                useful_data = {
                    "title": item[0]["title"],
                    "description": item[0]["description"],
                    "isbn13": item[0]["isbn13"],
                    "publisher": item[0]["publisher"],
                    "price": item[0]["priceStandard"],
                    "pub_date": datetime.datetime.strptime(
                        item[0]["pubDate"], "%Y-%m-%d"
                    ),
                    "author": item[0]["author"],
                }
                img_url = item[0]["cover"]

                response_time = datetime.datetime.now()
                book = Book(
                    **useful_data,
                    datetime=response_time,
                    cover="",
                    created_at=response_time
                )
                await mongo_db.engine.save(book)

                request_object.response_date = response_time
                request_object.response_id = str(book.id)
                request_object.response_code = 201
                await mongo_db.engine.save(request_object)

            else:
                response_time = datetime.datetime.now()
                request_object.response_date = response_time
                request_object.response_code = 404
                await mongo_db.engine.save(request_object)
