from bson import ObjectId
import logging

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoManager:
    def __init__(self):
        self._client: AsyncIOMotorClient = None
        self._db: AsyncIOMotorDatabase = None

    def init_motor(self, app: FastAPI, dsn: str):
        self.dsn = dsn

        @app.on_event("startup")
        def startup():
            logging.info("Connecting to MongoDB")
            self.client = AsyncIOMotorClient(self.dsn, maxPoolSize=10, minPoolSize=10)
            self.db = self.client.main_db
            logging.info("Connected to MongoDB")
            self.connect_db(self.path)

        @app.on_event("shutdown")
        def shutdown():
            logging.info("Closing connection with MongoDB")
            self.client.close()
            logging.info("Closed connection with MongoDB")

    def get_db(self):

        try:
            yield self.client
        finally:
            self._client.close()

    @property
    def session(self) -> function:
        return self.get_db
