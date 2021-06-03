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

def aladin_api(isbn_str: str) -> Dict:

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

