"""
Custom Aladin BookStore API Parser
==================================

알라딘 api를 이용하여 isbn(10자리, 13자리) 검색을 통해 책 정보를 가져옵니다.
기본 사용법:

>> adadin.isbn_requests()

개요:
isbn requests 로 요청하기
json을 dict으로 만들기
이미지 다운받기
dict 리턴

필요사항:
.env에 api를 요청할 수 있는 client key 정보가 있어야 합니다.
"""

from io import BytesIO
from typing import Dict

import requests
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as elemTree
from pathlib import Path
from PIL import Image
import re
import json

load_dotenv()

class AladinApiException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"[알라딘 API ERROR]: {self.msg}"


def download_thumbnail(url: str, isbn13: str) -> Path:
    """이미지 url을 thumnail 폴더에 저장하는 함수

    :param
    """
    res = requests.get(url)
    bytes_img = res.content
    img = Image.open(BytesIO(bytes_img))
    img.save(f"thumbnails/{isbn13}.jpg")

    return Path(__file__).resolve().parent / "thumbnails" / isbn13 / ".jpg"


def isbn_dict(isbn_str: str) -> Dict:

    url = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"
    ttbkey = os.environ["ttbkey"]

    if (str_len := len(isbn_str)) == 10:
        isbn_type = "ISBN"
    elif str_len == 13:
        isbn_type = "ISBN13"
    else:
        raise AladinApiException("isbn string 길이가 맞지 않습니다.")

    res: requests.Response = requests.post(
        url,
        data={
            "TTBKey": ttbkey,
            "itemIdType": isbn_type,
            "ItemId": isbn_str,
            "Cover": "Big",
            "output": "js",
        },
    )

    if res.status_code != 200:
        raise AladinApiException("알라딘 API를 정상적으로 이용할 수 없습니다.")

    if re.findall("(errorCode|errorMessage)", res.text):
        raise AladinApiException("상품정보가 알라딘에 존재하지 않습니다.")

    data: Dict = json.loads(res.text[:-1])["item"][0]
    download_thumbnail(data["cover"], data["isbn13"])

    return data
