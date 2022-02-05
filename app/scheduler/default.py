import logging
from fastapi import FastAPI

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.memory import MemoryJobStore


logger = logging.getLogger("scheduler")


class MyScheduler:
    def __init__(self, app: FastAPI = None, **kwargs):
        self._scheduler = None
        if app is not None:
            self.init_scheduler(app=app, **kwargs)

    def init_scheduler(self, app: FastAPI, **kwargs):
        mongo_url = kwargs.get("MONGO_URL")
        if not mongo_url:
            # TODO: raise exception
            pass
        jobstores = {
            "mongo": MongoDBJobStore(url=mongo_url),
        }
        self._scheduler = AsyncIOScheduler(timezone="Asia/Seoul", jobstores=jobstores)

        @app.on_event("startup")
        def startup():
            self._scheduler.start()
            logger.info("Created Schedule Object")

        @app.on_event("shutdown")
        def shutdown():
            pass
