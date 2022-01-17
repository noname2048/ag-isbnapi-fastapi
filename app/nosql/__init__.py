from app.settings.base import REPO_DIR
from app.settings import config

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import asyncio

try:
    _mongo_db_name = config.get("MONGO_DB")
    _mongo_db_password = config.get("MONGO_PASSWORD")
    _mongo_db_user = config.get("MONGO_USER")
except KeyError:
    raise EnvironmentError("cannot find MONGO_DB from '.env' file")


class _MongoDB:
    def __init__(self):
        self.client = None
        self.__engine = None

    async def connect(self) -> AsyncIOMotorClient:
        if not self.client:
            self.client = AsyncIOMotorClient(
                f"mongodb+srv://{_mongo_db_user}:{_mongo_db_password}@cluster0.zywhp.mongodb.net/{_mongo_db_name}?retryWrites=true&w=majority"
            )
            self.__engine = AIOEngine(
                motor_client=self.client, database=f"{_mongo_db_name}"
            )
            return self.client
        return self.client

    async def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    @property
    async def engine(self):
        if not self.client:
            await self.connect()

        return self.__engine

    @engine.setter
    def engine(self, value):
        self.__engine = value

    async def __del__(self):
        if self.client:
            await self.disconnect()


mongo_db = _MongoDB()


async def connect_db():
    await mongo_db.connect()


async def close_db():
    await mongo_db.close()
