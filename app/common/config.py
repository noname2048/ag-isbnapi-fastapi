from typing import List, Union
from os import environ
from pathlib import Path
from dataclasses import dataclass, asdict
from functools import lru_cache

from pydantic import BaseSettings
from dotenv import dotenv_values

config_dir = Path(__file__).resolve().parent
base_dir = config_dir.parent
secrets = dotenv_values(config_dir / ".env")


@dataclass
class Config:
    """기본적인 Config"""

    BASE_DIR = base_dir


@dataclass
class LocalConfig(Config):
    ALLOWED_ORIGIN = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ]  # QUESTION: if type noticed, error occurs
    POSTGRES_URL: str = (
        f"postgresql+psycopg2://{secrets['POSTGRESQL_USER']}:{secrets['POSTGRESQL_PW']}"
        f"@{'localhost'}:{'5432'}/{secrets['POSTGRESQL_DBNAME']}"
    )
    POSTGRES_ECHO: bool = True
    MONGODB_URL: str = ()


@dataclass
class ProdConfig(Config):
    pass


def get_config() -> Union[LocalConfig, ProdConfig]:
    """
    API_ENV 설정에 따라 설정값을 가져옵니다. (default=local)

    :return: LocalConfig | ProdConfig
    """
    config = dict(prod=ProdConfig, local=LocalConfig)
    return config[environ.get("API_ENV", "local")]


def get_postgresql_url(*, secrets: dict) -> str:
    """
    시크릿으로 부터 키값을 추출하여 db url을 리턴합니다.

    :return: db_url
    """
    POSTGRESQL_USER = secrets["POSTGRESQL_USER"]
    POSTGRESQL_PW = secrets["POSTGRESQL_PW"]
    HOST = "localhost"
    PORT = "8000"
    POSTGRESQL_DBNAME = secrets["POSTGRESQL_DBNAME"]

    return (
        f"postgresql+psycopy2:"
        f"//{POSTGRESQL_USER}:{POSTGRESQL_PW}"
        f"@{HOST}:{PORT}/{POSTGRESQL_DBNAME}"
    )


def get_mongodb_url(*, secrets: dict) -> str:
    MONGODB_USER = secrets["MONGODB_USER"]
    MONGODB_PW = secrets["MONGODB_PW"]
    MONGODB_DBNAME = secrets["MONGODB_DBNAME"]

    return (
        f"mongodb+srv:"
        f"//{MONGODB_USER}:{MONGODB_PW}"
        f"@cluster0.zywhp.mongodb.net/{MONGODB_DBNAME}"
        f"?retryWrites=true&w=majority"
    )


class Settings(BaseSettings):
    BASE_DIR: Path = base_dir
    ALLOWED_ORIGIN: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ]
    POSTGRESQL_URL: str = get_postgresql_url(secrets=secrets)
    POSTGRESQL_ECHO: bool = True
    MONGODB_URL: str = get_mongodb_url(secrets=secrets)


@lru_cache()
def get_settings():
    return Settings()
