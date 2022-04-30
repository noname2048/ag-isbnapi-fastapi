from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from app.odmantic import get_engine
from app.odmantic.models import Request, RequestForm
from app.task.crawl import f2
from app.utils.logger import mylogger

from app.task.v2.response import respond_single_request


def init_repeat_crawl(app: FastAPI):
    """register starup event"""

    @app.on_event("startup")
    @repeat_every(seconds=180)
    async def bulk_respond():
        mylogger.info("checking db...")
        engine = get_engine()
        rf_list = await engine.find(
            RequestForm,
            RequestForm.response_date == None,
            limit=20,
        )
        # if not rf_list:
        #     mylogger.info("checking done")
        # else:
        num = len(rf_list)
        for idx, rf in enumerate(rf_list):
            await respond_single_request(rf.id)
            mylogger.info(f"{ rf.isbn } ({idx + 1}/{num})")
