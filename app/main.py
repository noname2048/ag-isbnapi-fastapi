import uvicorn
from fastapi import FastAPI, APIRouter

from app.routers.request import router as request_router
from app.routers.books import router as books_router
from app.routers.search import router as search_router
from app.routers.auth import router as auth_router
from app.routers.oauth import router as oauth_router

# api
# 요청하고 -> 나열하고 -> 검색하고
router = APIRouter(tags=["api/v1"], prefix="/api/v1")
router.include_router(request_router, tags=["request"], prefix="/request")
router.include_router(search_router, tags=["search"], prefix="/search")
router.include_router(books_router, tags=["books"], prefix="/books")

# app
app = FastAPI()
app.include_router(router)


# main
@app.get("/")
async def hello():
    return {"messege": "hello"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
