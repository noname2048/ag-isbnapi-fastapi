from pydantic import HttpUrl
import aiohttp
import boto3
from app.settings import config


async def upload(isbn13: int, img_url: HttpUrl):
    """img url을 받아 S3에 업로드 한후 결과를 리턴하는 함수"""

    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            if response.status != 200:
                return False

            img_data = await response.read()
            s3 = boto3.resource(
                "s3",
                region_name="ap-northeast-2",
                aws_access_key_id=config["aws_id"],
                aws_secret_access_key=config["aws_key"],
            )
            bucket = s3.Bucket("job-book-image")
            obj = bucket.Object(f"{isbn13}.jpg")
            await obj.upload_fileobj(img_data)

            return True
