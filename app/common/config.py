"""
config.py

서버를 구동하는데 있어 필요한 설정값은 모두 해당 파일에 기재
민감한 정보는 .env에 따로 적되, 여기서 불러와서 저장

현 파일에는 dataclass를 이용하는 '방법1'과 (차후 attrs로 업데이트)
pydantic의 BaseSettings를 이용하는 '방법2'가 혼재
"""
from typing import List, Union
from os import environ
from pathlib import Path
from dataclasses import dataclass, asdict
from functools import lru_cache

from pydantic import BaseSettings, Field
from dotenv import dotenv_values

from app.common.consts import EXCEPT_PATH_LIST

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
    TRUSTED_HOSTS = ["*"]


@dataclass
class ProdConfig(Config):
    pass


@lru_cache()
def get_config() -> Union[LocalConfig, ProdConfig]:
    """
    API_ENV 설정에 따라 설정값을 가져옵니다. (default=local)

    :return: LocalConfig | ProdConfig
    """
    config = dict(prod=ProdConfig(), local=LocalConfig())
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
    """
    pydantic의 문서를 참조하여 작성된 fastapi 기본 설정

    나중에 다시 봐도 딱 알 수 있도록 상세히 기재
    소문자로 바꿔야 하는지 고민 중
    """

    BASE_DIR: Path = base_dir
    ALLOWED_ORIGIN: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ]
    AUTHORIZATION_EXCEPT_ENDPOINT_LIST: list = [
        "/",
        "/health",
        "/openapi.json",
    ]
    AUTHORIZATION_EXCEPT_ENDPOINT_REGEX: str = "^(/docs|/redoc|/auth)"
    # DSN은 Data Source Name을 뜻함
    POSTGRESQL_DSN: str = get_postgresql_url(secrets=secrets)
    POSTGRESQL_ECHO: bool = True
    MONGODB_DSN: str = get_mongodb_url(secrets=secrets)
    # JWT_SECRET은 공개가 어려움
    JWT_SECRET: str = Field(..., env="BASE_JWT_SECRET")
    JWT_ALGORITHM: str = Field(..., env="BASE_JWT_ALGORITHM")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
