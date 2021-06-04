"""
Custom Aladin BookStore API Parser
==================================

알라딘 api를 이용하여 isbn(10자리, 13자리) 검색을 통해 책 정보를 가져옵니다.
기본 사용법:

>> adadin.isbn_dict()

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

load_dotenv()


def aladin_parse(res: requests.Response) -> Dict:
    """알리딘 파이프라인 중 response(xml)을 Dict 로 바꾸는 과정

    """
    ret = dict()

    tree = elemTree.fromstring(res.text)
    if tree.find("error"):
        return ret

    for elem in tree.find("object/item"):
        ret[elem.tag] = elem.text

    return ret

def download_thumbnail(url: str, isbn13: str) -> Path:

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

    res: requests.Response = requests.post(
        url,
        data={
            "TTBKey": ttbkey,
            "itemIdType": isbn_type,
            "ItemId": isbn_str,
            "Cover": "Big",
        },
    )

    if res.status_code != 200:
        return {}

    res_dict: Dict = aladin_parse(res)
    if not res_dict:
        return {}

    download_thumbnail(res["cover"], res["isbn13"])

