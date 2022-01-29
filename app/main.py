from datetime import datetime, timedelta
import asyncio
import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from app.books import router as books_router
from app.nosql.odmantic import connect_db, close_db
from app.common.config import conf

from apscheduler.schedulers.asyncio import AsyncIOScheduler

# from app.task.myscheduler import find_not_responded_request


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


async def startup():
    at = datetime.now()
    print(f"server starts at {datetime.now()}")

    # app.scheduler = AsyncIOScheduler(timezone="Asia/Seoul")
    # app.scheduler.add_job(simple_print, "date", run_date=at + timedelta(seconds=30))
    # app.scheduler.add_job(simple_print, "cron", second=20)

    # # app.scheduler.add_job(find_not_responded_request, "interval", minutes=1)
    await connect_db()


async def shutdown():
    await close_db()


app.add_event_handler("startup", connect_db)
app.add_event_handler("shutdown", close_db)


async def simple_print():
    print("background task: ", datetime.now())


@app.get("/")
async def hello():
    return {"messege": "hello"}


if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # config = uvicorn.Config(
    #     "app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4
    # )
    # server = uvicorn.Server(config)
    # loop.run_until_complete(server.serve())

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True, workers=4)


def create_app():
    """fastapi 앱을 만드는 함수"""
    c = conf()
    app = FastAPI()
    # DB
    # redis
    # middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:8000",
            "http://localhost",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    # router
    app.router.include_router(books_router, tags=["books"], prefix="/books")
    return app


if False:
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
