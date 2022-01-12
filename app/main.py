import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.books import router as books_router
from app.nosql import connect_db, close_db

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.task.myscheduler import find_not_responded_request

router = APIRouter(tags=["api/v1"], prefix="/api/v1")
router.include_router(books_router, tags=["books"], prefix="/books")


origins = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://localhost",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)
app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)

app.scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
app.scheduler.add_job(find_not_responded_request, "interval", minutes=1)
app.scheduler.start()


@app.get("/")
async def hello():
    return {"messege": "hello"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)
