"""api error catch를 위한 logger 
"""
from fastapi.logger import logger
from fastapi import Request
from inspect import currentframe as frame
from pydantic import BaseModel

UVICORN_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": "%(levelname)s %(name)s@%(lineno)d %(message)s",
        },
    },
    "handlers": {"default": {"formatter": "default", "class": "m"}},
}


class LogConfig(BaseModel):
    LOGGER_NAME = "isbnapi"
    # LOG_FORMAT = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_FORMAT = "%(levelprefix)s %(client_addr)s  | %(asctime)s | %(message)s"
    LOG_LEVEL = "DEBUG"

    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "isbnapi": {"handlers": ["default"], "level": LOG_LEVEL},
    }


dict_config = LogConfig().dict()


async def api_error_logger(request: Request, response=None, error=None):

    pass