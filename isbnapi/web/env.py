from functools import lru_cache
from pydantic import BaseSettings
from pathlib import Path

APP_DIR: str = Path(__file__).parent.parent


class Setting(BaseSettings):
    ttbkey: str

    class Config:
        env_file = APP_DIR / ".env"


@lru_cache
def get_setting():
    setting = Setting()
    return setting
