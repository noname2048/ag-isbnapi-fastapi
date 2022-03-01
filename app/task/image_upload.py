from pydantic import HttpUrl
import aiohttp
import boto3
from app.settings import config
from app.utils.singleton_session import session
import requests
import re
from botocore.exceptions import ClientError

s3 = boto3.resource(
    "s3",
    region_name="ap-northeast-2",
    aws_access_key_id=config["aws_id"],
    aws_secret_access_key=config["aws_key"],
)
bucket = s3.Bucket("job-book-image")


async def upload(isbn13: int, img_url: HttpUrl):
    """img url을 받아 S3에 업로드 한후 결과를 리턴하는 함수"""

    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            if response.status != 200:
                return False

            img_data = await response.read()
            # s3 = boto3.resource(
            #     "s3",
            #     region_name="ap-northeast-2",
            #     aws_access_key_id=config["aws_id"],
            #     aws_secret_access_key=config["aws_key"],
            # )
            # bucket = s3.Bucket("job-book-image")
            obj = bucket.Object(f"{isbn13}.jpg")
            await obj.upload_fileobj(img_data)

            return True


async def upload_when_not_exists(isbn13: str, img_url: HttpUrl) -> bool:
    global s3, bucket

    # isbn 형식확인
    isbn_pattern = re.compile(r"^\d{13}$")
    if not isbn_pattern.match(isbn13):
        raise Exception("isbn13")

    # response status code 확인
    response = requests.get(img_url)
    if response.status_code != 200:
        raise Exception("img_url not valid")

    # 파일이 이미 존재하는지 확인
    obj = bucket.Object(f"{isbn13}.jpg")
    try:
        obj.load()
    except ClientError as e:
        if e.response["Error"]["Code"] == 404:
            raise Exception("file already exists")
        raise Exception("unknwon Error")

    obj.upload_fileobj(response.raw)
    return True
