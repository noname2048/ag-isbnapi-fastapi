from config import get_secret
from typing import Optional
import aiohttp
import asyncio


async def fetch(session: aiohttp.ClientSession, url: str, i: int):
    headers = {
        "X-Naver-Client-Id": get_secret("client_id"),
        "X-Naver-Client_secret": get_secret("client_secret"),
    }
    async with session.get(url, headers=headers) as response:
        result = await response.json()
        items = result["items"]
        images = [item["link"] for item in items]
        print(images)


async def main():
    BASE_URL = "https://openapi.naver.com/v1/search/image"
    keyword = "cat"
    urls = [
        f"{BASE_URL}?query={keyword}&display=20&start={1 + i*20}" for i in range(10)
    ]
    async with aiohttp.ClientSEssion() as session:
        await asyncio.gather(*[fetch(session, url, i) for i, url in enumerate(urls)])


if __name__ == "__main__":
    asyncio.run(main())
