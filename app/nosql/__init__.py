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
    def __init__(self):
        self.client = None
        self.engine = None
        self.connect()

    def connect(self):
        if not self.client:
            self.client = AsyncIOMotorClient(
                f"mongodb+srv://{_mongo_db_user}:{_mongo_db_password}@cluster0.zywhp.mongodb.net/{_mongo_db_name}?retryWrites=true&w=majority"
            )
            self.engine = AIOEngine(
                motor_client=self.client, database=f"{_mongo_db_name}"
            )

    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

    def __del__(self):
        self.disconnect()


mongo_db = _MongoDB()
