from fastapi import FastAPI
from dotenv import load_dotenv

from pymongo import MongoClient
import aladin

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

    ret = books_collection.find_one({"isbn": isbn})
    if ret is not None:
        ret.pop("_id")
        return ret

    try:
        data = aladin.isbn_dict(isbn)
    except aladin.AladinApiException as e:
        return { "error": e.msg }

    books_collection.insert_one(data)
    data.pop("_id")
    return data

@app.get("/test")
async def test():
    db = client["api"]
    mycol = db.book
    x = mycol.find_one({"isbn": "9791158392239"})
    x.pop("_id")

    return x
