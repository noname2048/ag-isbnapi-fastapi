from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import Request
from app.task.crawl import f2
from app.utils.logger import mylogger


def init_repeat_crawl(app: FastAPI):
    @app.on_event("startup")
    @repeat_every(seconds=5 * 60)
    async def repeat_crawl() -> None:
        mylogger.info("start repeat crawl!")
        engine = singleton_mongodb.engine
        requests = await engine.find(
            Request,
            Request.status.in_(["requested", "need update"]),
            limit=100,
        )

        if not requests:
            mylogger.info("no requests find! - crawl end")

        else:
            request_len = len(requests)
            mylogger.warn(f"start crawl {request_len}")

            books = await f2(requests)

            book_len = len(books)
            mylogger.info(f" repeat crawl end!")
