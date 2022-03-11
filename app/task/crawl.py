import requests
import re
import json
from datetime import datetime
from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request, Book


aladin_api_url = ""
ttbkey = ""
isbn13_pattern = re.compile(r"^\d{13}$")


async def f1(mongo_object_id: str):
    engine = singleton_mongodb.engine
    request = await engine.find_one(Request, Request.id == mongo_object_id)
    if not request:
        raise Exception()

    isbn13 = request.isbn
    if not isbn13_pattern.match(isbn13):
        raise Exception()

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

    try:
        text = response.text[:-1]
        json_data = json.loads(text, strict=False)
        item = json_data.get("item", None)
    except json.decoder.JSONDecodeError:
        request.status = "json error"
        await engine.save(request)
        raise Exception("")

    if not item:
        request.status = "item not found"
        await engine.save(request)
        raise Exception()

    book_data = {
        "title": item[0]["title"],
        "description": item[0]["description"],
        "isbn13": item[0]["isbn13"],
        "publisher": item[0]["publisher"],
        "price": item[0]["priceStandard"],
        "pub_date": datetime.datetime.strptime(item[0]["pubDate"], "%Y-%m-%d"),
        "author": item[0]["author"],
        "cover": f"{request['isbn']}.jpg",
    }

    # check aws
    # if not, upload

    Book(validate=False)
    Book.title
    Book.description
    Book.isbn13
    Book.pub_date
    Book.publisher
    Book.price
    Book.author
    Book.cover
