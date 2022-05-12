from fastapi import FastAPI
from isbnapi.auth import authentication
from isbnapi.routes import user, missing_book, book
from isbnapi.db import models
from isbnapi.db.database import engine

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(missing_book.router)
app.include_router(book.router)


@app.get("/")
async def index():
    return "Hello World"


models.Base.metadata.create_all(engine)
