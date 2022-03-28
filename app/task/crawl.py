import requests
import re
import json
from datetime import datetime, timedelta

from boto3 import resource

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request, Book
from app.common.config import settings
from app.exceptions import crawl_error

aladin_api_url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
ttbkey = settings.aladin_ttbkey
isbn13_pattern = re.compile(r"^\d{13}$")


async def f1(mongo_object_id: str):

    # parameter를 바탕으로 request 불러오기
    engine = singleton_mongodb.engine
    request = await engine.find_one(Request, Request.id == mongo_object_id)
    if not request:
        raise crawl_error.MongoObjectNotFound()

    isbn13 = request.isbn
    if not isbn13_pattern.match(isbn13):
        raise crawl_error.IsbnPatternError()

    # 알라딘에 isbn13으로 요청
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
        raise crawl_error.AladinResponseError("알라딘에서 200이 아닌 응답을 수신")

    # 반환받은 text를 json으로 변경
    try:
        text = response.text[:-1]
        json_data = json.loads(text, strict=False)
        item = json_data.get("item", None)
    except json.decoder.JSONDecodeError:
        request.status = "json error"
        await engine.save(request)
        raise crawl_error.AladinResponseError()

    if not item:
        request.status = "item not found"
        await engine.save(request)
        raise crawl_error.AladinItemNotFound()

    # 변환된 json에서 필요한 book 데이터 추출
    img_url = item[0]["cover"]
    new_book = Book(
        title=item[0]["title"],
        description=item[0]["description"],
        isbn13=item[0]["isbn13"],
        publisher=item[0]["publisher"],
        price=item[0]["priceStandard"],
        pub_date=datetime.strptime(item[0]["pubDate"], "%Y-%m-%d"),
        author=item[0]["author"],
        cover=f"{isbn13}.jpg",
        created_at=datetime.utcnow() + timedelta(hours=9),
        updated_at=datetime.utcnow() + timedelta(hours=9),
    )

    # cover 이미지가 aws에 있는지 확인
    bucket = resource(
        "s3",
        region_name="ap-northeast-2",
        aws_access_key_id=settings.boto3_aws_access_id,
        aws_secret_access_key=settings.boto3_aws_access_key,
    ).Bucket("job-book-image")
    obj = bucket.Object(new_book.cover)

    try:
        obj.load()
    except Exception as e:
        if e.response["Error"]["Code"] == 404:
            img_res = requests.get(img_url)
            obj.upload_fileobj(img_res.raw)

    saved_book = await engine.save(new_book)
    return saved_book
