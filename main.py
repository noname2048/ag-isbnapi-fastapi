from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as elemTree
import xmltodict
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import json

client = MongoClient("mongodb://root:example@mongo:27017")
print(client.list_database_names())
db = client["api"]
books_collection = db.book

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/isbn/{isbn}")
async def isbn(isbn: str):

    if (ret := books_collection.find_one({"isbn": isbn})) is not None:
        ret.pop("_id")
        return ret

    r: requests.Response = requests.get(
        "https://openapi.naver.com/v1/search/book_adv.xml",
        headers={
            (client_id := "X-Naver-Client-Id"): os.environ[client_id],
            (client_secret := "X-Naver-Client-Secret"): os.environ[client_secret],
        },
        params={"d_isbn": isbn},
    )

    tree = elemTree.fromstring(r.text)
    data = dict()
    for elem in list(tree.find('channel/item')):
        data[elem.tag] = elem.text
    data['isbn'] = data['isbn'].split(' ')[-1]
    
    img_link = data['image']
    res = requests.get(img_link)
    bytes_img = res.content
    img = Image.open(BytesIO(bytes_img))
    img.save(f"thumbnails/{isbn}.jpg")

    books_collection.insert_one(data)

    return data


@app.get("/test")
async def test():
    db = client["api"]
    mycol = db.book
    x = mycol.find_one({"isbn": "9791158392239"})
    x.pop("_id")

    return x
