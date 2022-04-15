import asyncio
from bson import ObjectId

from app.settings.base import REPO_DIR
from app.settings import config

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

try:
    _mongo_db_name = config.get("MONGO_DB")
    _mongo_db_password = config.get("MONGO_PASSWORD")
    _mongo_db_user = config.get("MONGO_USER")
    _mongo_db_url = config["MONGO_URL"]
except KeyError:
    raise EnvironmentError("cannot find MONGO_DB from '.env' file")


class MoterMongo:
    def __init__(self):
        self.client = AsyncIOMotorClient(_mongo_db_url)
        self.db = self.client.isbn


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class _MongoDB:
    def __init__(self):
        self.client = None
        self.engine = None

    def __del__(self):
        if self.client:
            self.disconnect()

    def connect(self) -> AsyncIOMotorClient:
        if not self.client:
            self.client = AsyncIOMotorClient(
                f"mongodb+srv://{_mongo_db_user}:{_mongo_db_password}@cluster0.zywhp.mongodb.net/{_mongo_db_name}?retryWrites=true&w=majority"
            )
            self.engine = AIOEngine(
                motor_client=self.client, database=f"{_mongo_db_name}"
            )
            return self.client
        return self.client

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        if exc_type:
            return False
        return True


mongo_db = _MongoDB()


async def connect_db():
    mongo_db.connect()


async def close_db():
    mongo_db.close()
