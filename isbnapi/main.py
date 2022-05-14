from fastapi import FastAPI
from isbnapi.auth import authentication
from isbnapi.routes import user, missing_book, book
from isbnapi.db import models
from isbnapi.db.database import engine
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(missing_book.router)
app.include_router(book.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return "Hello World"


app.mount("/bookimages", StaticFiles(directory="isbnapi/bookimages"), name="bookimages")
models.Base.metadata.create_all(engine)
