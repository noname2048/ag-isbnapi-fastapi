from app.settings.base import REPO_DIR
from app.settings import config

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

try:
    _mongo_db_name = config.get("MONGO_DB")
    _mongo_db_password = config.get("MONGO_PASSWORD")
    _mongo_db_user = config.get("MONGO_USER")
except KeyError:
    raise EnvironmentError("cannot find MONGO_DB from '.env' file")


class _MongoDB:
    # __instance = None

    # def __new__(cls, *args, **kwargs):
    #     if not cls.__instance:
    #         cls.__instance = super().__new__(cls, *args, **kwargs)
    #     return cls.__instance

    def __init__(self):
        self.client = None
        self.engine = None

    def connect(self):
        self.client = AsyncIOMotorClient(
            f"mongodb+srv://{_mongo_db_user}:{_mongo_db_password}@cluster0.zywhp.mongodb.net/{_mongo_db_name}?retryWrites=true&w=majority"
        )
        self.engine = AIOEngine(motor_client=self.client, database=f"{_mongo_db_name}")

    def close(self):
        self.client.close()

    def __del__(self):
        # self.close()
        pass


mongo_db = _MongoDB()
mongo_db.connect()
