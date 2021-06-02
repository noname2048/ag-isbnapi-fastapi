from fastapi import FastAPI
import requests
from dotenv import load_dotenv
import os
import xml.etree.ElementTree as elemTree
import xmltodict
from PIL import Image
from io import BytesIO

load_dotenv()
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/isbn/{isbn}")
async def isbn(isbn: str):

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

    return data
