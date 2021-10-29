import pymongo
from dotenv import dotenv_values
from pathlib import Path
import requests
import json
from PIL import Image
from io import BytesIO
from typing import Dict


# env에서 설정값 가지고 오기
DIR = Path(__file__)
config = dotenv_values(DIR.parent / ".env")
password = config["MONGO_PASSWORD"]
db_name = config["MONGO_DB"]
client = pymongo.MongoClient(
    f"mongodb+srv://swook:{password}@cluster0.zywhp.mongodb.net/{db_name}?retryWrites=true&w=majority"
)
col = client.isbn.book

# 알라딘 추가설정
ttbkey = config["ALADIN_TTB_KEY"]
url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"


async def get_images(image_url, name) -> Image.Image:
    res = requests.get(image_url)
    bytes_img = res.content
    img = Image.open(BytesIO(bytes_img))

    if name:
        img.save(name)

    return img


async def aladin_api_query(isbn13) -> Dict:
    """알라딘에서 받은 정보를 저장하기"""
    res = requests.post(
        url,
        data={
            "TTBKey": ttbkey,
            "itemIdType": "ISBN13",
            "ItemId": isbn13,
            "Cover": "Big",
            "output": "js",
        },
    )

    if res.status_code != 200:
        print("Adadin API Error: status code is not 200")
        return {}

    origin = json.loads(res.text[:-1], strict=False)
    item = origin["item"][0]
    keywords = [
        "title",
        "description",
        "isbn13",
        "cover",
        "publisher",
        "priceSales",
        "pubDate",
        "author",
    ]
    data = {}
    for keyword in keywords:
        data[keyword] = item[keyword]

    # 이미지 저장
    img_name = data["isbn13"] + ".jpg"
    _ = await get_images(data["cover"], img_name)
    data["cover"] = img_name

    return data


async def query_and_register(isbn13: str):
    q = col.find_one({"isbn13": isbn13})
    if q:
        return [q, "existed"]

    book = await aladin_api_query(isbn13)
    book_id = col.insert_one(book).inserted_id

    return [book, "new"]
