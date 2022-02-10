from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient


class MongoDB:
    def __init__(self):
        self._client: AsyncIOMotorClient = None

    def init_motor(self, app: FastAPI, dsn: str):
        self.dsn = dsn

        @app.on_event("startup")
        def startup():
            self._client = AsyncIOMotorClient(self.dsn)

        @app.on_event("shutdown")
        def shutdown():
            self._client.close()

    @property
    def client(self):
        if not self._client:
            raise Exception("use mongodb before init")

        return self._client


mongodb = MongoDB()
