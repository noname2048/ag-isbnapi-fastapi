from typing import Tuple, Any
import requests
from dotenv import dotenv_values
from isbnapi.web.env import get_setting
from fastapi import HTTPException, status
import json
from isbnapi.schemas import BookBase
from datetime import date, datetime
from pathlib import Path

setting = get_setting()
ALADIN_API_ENDPOINT = "http://www.aladin.co.kr/ttb/api/ItemLookUp.aspx"


def get_bookinfo(isbn: str, missingbook_id: int) -> Tuple[bool, Any]:
    response = requests.post(
        url=ALADIN_API_ENDPOINT,
        data={
            "TTBKey": setting.ttbkey,
            "itemIdType": "isbn13",
            "ItemId": isbn,
            "Cover": "Big",
            "output": "js",
        },
    )

    if response.status_code != 200:
        return False, "Aladin not ok"

    text: str = response.text[:-1]
    try:
        _json = json.loads(text, strict=False)
        with open(
            Path(__file__).parent / "last_json.json", "w+", encoding="utf8"
        ) as buffer:
            json.dump(_json, buffer, ensure_ascii=False)
    except json.JSONDecodeError:
        with open(Path(__file__).parent / "last_text.txt", "w+") as buffer:
            buffer.write(text + "\n")
        return False, "Cannot parse json"

    if _json.get("errorCode", None):
        return False, _json.get("errorMessage", "Unknown aladin error")

    book = None
    try:
        target = _json["item"][0]
        _date = target["pubDate"].split("-")
        book_request = BookBase(
            isbn=target["isbn13"],
            title=target["title"],
            description=target["description"],
            cover=target["cover"],
            cover_type="absolute",
            publisher=target["publisher"],
            price=target["priceStandard"],
            pub_date=date(*map(int, _date)),
            author=target["author"],
            missingbook_id=missingbook_id,
        )
    except KeyError as e:
        return False, f"Keyerror {e.args[0]}"

    return True, book_request
