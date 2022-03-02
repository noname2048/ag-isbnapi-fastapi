from app.common.config import settings
from app.nosql.conn import mongodb
import requests
import json
from enum import Enum
import datetime
from app.task.image_upload import download_and_upload, is_in_s3, upload
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


async def single_crawl(requests_id: str):
    # requests 콜렉션의 docuemnt id 가져오기
    collection = mongodb.client["isbn"]["requests"]
    request = await collection.find_one({"_id": id})
    if not request:
        raise Exception("something wrong")
    isbn = request["isbn"]

    # 해당 isbn을 가지고 알라딘에 api 요청
    res = requests.post(
        aladin_api_url,
        {
            "TTBKey": ttb_key,
            "itemIdType": "isbn13",
            "ItemId": isbn,
            "Cover": "Big",
            "output": "js",
        },
    )

    # text를 json으로 변환
    try:
        text_result = res.text[:-1]
        json_result = json.loads(text_result, strict=False)
        item = json_result.get("item", None)
    except json.decoder.JSONDecodeError:
        temp = await collection.update_one({"_id": id}, {"status": "json error"})
        raise Exception("something wrong2")

    if not item:
        raise Exception("something wrong3")

    # 변환된 json에서 데이터 추출
    useful_data = {
        "title": item[0]["title"],
        "description": item[0]["description"],
        "isbn13": item[0]["isbn13"],
        "publisher": item[0]["publisher"],
        "price": item[0]["priceStandard"],
        "pub_date": datetime.datetime.strptime(item[0]["pubDate"], "%Y-%m-%d"),
        "author": item[0]["author"],
        "cover": f"{request['isbn']}.jpg",
    }

    # 체크하고 표지 다운받아 업로드
    if is_in_s3(item[0]["isbn13"]) == False:
        download_and_upload(item[0]["isbn13"], item[0]["cover"])

    # 몽고디비에 books 콜렉션에 문서 저장
    book_coll = mongodb.client["isbn"]["books"]
    inserted = await book_coll.insert_one(useful_data)
    new_book = await book_coll.find_one({"_id": inserted.inserted_id})

    return new_book
