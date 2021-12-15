from pathlib import Path as SysPath
import os
from dotenv import dotenv_values

from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

REPO_DIR = SysPath(__file__).resolve().parent.parent.parent
if not os.path.isdir(REPO_DIR / "app"):
    raise EnvironmentError("cannot find REPO_DIR directory")

_config = dotenv_values(REPO_DIR / ".env")
try:
    _mongo_db_name = _config.get("MONGO_DB")
    _mongo_db_password = _config.get("MONGO_PASSWORD")
    _mongo_db_user = _config.get("MONGO_USER")
except KeyError:
    raise EnvironmentError("cannot find MONGO_DB from '.env' file")


class _MongoDB:
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


mongo_db = _MongoDB()
