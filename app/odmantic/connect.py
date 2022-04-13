from typing import Optional
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient
from app.common.config import settings
from fastapi import FastAPI


class MongoDB:
    _client = None
    _engine = None

    def attach_event(self, app: FastAPI):
        @app.on_event("startup")
        def startup():
            self._client = AsyncIOMotorClient(settings.mongodb_dsn)
            self._engine = AIOEngine(
                motor_client=self._client, database=settings.mongodb_name
            )

        @app.on_event("shutdown")
        def shutdown():
            if self._client:
                self._client.close()

    @property
    def engine(self) -> AIOEngine:
        if not self._engine:
            raise Exception("mongodb engine not start")

        return self._engine


singleton_mongodb = MongoDB()
