import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.routers.request import router as request_router

# from app.routers.books import router as books_router
from app.books import router as books_router
from app.routers.search import router as search_router
from app.routers.auth import router as auth_router
from app.routers.oauth import router as oauth_router

from app.nosql import connect_db, close_db

# api
# 요청하고 -> 나열하고 -> 검색하고
router = APIRouter(tags=["api/v1"], prefix="/api/v1")
router.include_router(books_router, tags=["books"], prefix="/books")
# router.include_router(request_router, tags=["request"], prefix="/request")
# router.include_router(search_router, tags=["search"], prefix="/search")
# router.include_router(books_router, tags=["books"], prefix="/books")

# app
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
]

all = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=all,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

# async def get_mongodb_client() -> AsyncIOMotorClient:
#     pass


# async def connect_mongodb():
#     pass


# async def disconnect_mongodb():
#     pass


# main
@app.get("/")
async def hello():
    return {"messege": "hello"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
