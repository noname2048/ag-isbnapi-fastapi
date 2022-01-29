from distutils.command.config import config
from os import environ
from pathlib import Path
from dataclasses import dataclass, asdict

config_dir = Path(__file__).resolve().parent
base_dir = config_dir.parent


@dataclass
class Config:
    """기본적인 Config"""

    BASE_DIR = base_dir


@dataclass
class LocalConfig(Config):
    PROJ_RELOAD: bool = True
    DB_URL: str = ""


@dataclass
class ProdConfig(Config):
    PROJ_RELOAD: bool = False


def conf():
    config = dict(prod=ProdConfig, local=LocalConfig())
    return config.get(environ.get("API_ENV", "local"))
