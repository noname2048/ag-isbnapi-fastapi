from bson import ObjectId
import logging

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase


class MongoManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    def __init__(self, app: FastAPI, **kwargs):
        self.path = kwargs.get("path")
        if app is not None:

            @app.on_event("startup")
            def startup():
                self.connect_db(self.path)

            @app.on_event("shutdown")
            def shutdown():
                self.close_db()

    async def connect_db(self, path: str):
        logging.info("Connecting to MongoDB")
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client.main_db
        logging.info("Connected to MongoDB")

    async def close_db(self):
        logging.info("Closing connection with MongoDB")
        self.client.close()
        logging.info("Closed connection with MongoDB")
