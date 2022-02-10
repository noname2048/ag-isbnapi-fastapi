"""
config.py

서버를 구동하는데 있어 필요한 설정값은 모두 해당 파일에 기재
민감한 정보는 .env에 따로 적되, 여기서 불러와서 저장

현 파일에는 dataclass를 이용하다가 list[str]을 사용할 수 없어
attrs 패키지로 업그레이드 하려다가, 
pydantic의 BaseSettings를 이용하는 '방법2'를 채택
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


class Settings(BaseSettings):
    """
    pydantic의 문서를 참조하여 작성된 fastapi 기본 설정

    나중에 다시 봐도 딱 알 수 있도록 상세히 기재
    """

    base_dir: Path = base_dir
    allowed_origin: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost",
    ]
    authorization_except_list: list = [
        "/",
        "/health",
        "/openapi.json",
    ]
    authorization_except_regex: str = "^(/docs|/redoc|/auth)"
    postgresql_dsn: str = "postgresql+psycopy2://user:password@localhost:5432/test"
    postgresql_echo: bool = True
    mongodb_dsn: str = "mongodb+srv://user:password@localhost:27017/test"
    jwt_secret: str = "4321dcba"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = config_dir / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
