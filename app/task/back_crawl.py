from app.common.config import settings
from app.nosql.conn import mongodb
import requests
import json
from enum import Enum
import datetime
from app.task.image_upload import upload
import asyncio


class SessionManager:
    def __init__(self):
        self.session = None

    async def make_session(self):
        if self.session:
            return
        # self.session = await
        pass


class crawlErrorType(Enum, str):
    requested: str = "requested"
    json_error: str = "json_error"


aladin_api_url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
ttb_key = settings.aladin_ttbkey


async def single_crawl(id: str):
    collection = mongodb.client["isbn"]["requests"]
    request = await collection.find_one({"_id": id})
    if not request:
        raise Exception("something wrong")

    res = requests.post(
        aladin_api_url,
        {
            "TTBKey": ttb_key,
            "itemIdType": "isbn13",
            "ItemId": str(request["isbn"]),
            "Cover": "Big",
            "output": "js",
        },
    )
    try:
        text_result = res.text[:-1]
        json_result = json.loads(text_result, strict=False)
        item = json_result.get("item", None)
    except json.decoder.JSONDecodeError:
        temp = await collection.update_one({"_id": id}, {"status": "json error"})
        raise Exception("something wrong2")

    if not item:
        raise Exception("something wrong3")

    useful_data = {
        "title": item[0]["title"],
        "description": item[0]["description"],
        "isbn13": item[0]["isbn13"],
        "publisher": item[0]["publisher"],
        "price": item[0]["priceStandard"],
        "pub_date": datetime.datetime.strptime(item[0]["pubDate"], "%Y-%m-%d"),
        "author": item[0]["author"],
    }
    # 이미 있으면 안올리는 로직 추가하기
    await upload(request["isbn"], item[0]["cover"])

    useful_data["cover"] = f"{request['isbn']}.jpg"

    book_coll = mongodb.client["isbn"]["books"]
    await book_coll.insert_one(useful_data)
