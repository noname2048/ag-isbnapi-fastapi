from venv import create
from numpy import disp
import uvicorn

from fastapi import FastAPI  # ,APIRouter

# from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from app.common.config import settings

# from app.middlewares.token_validator import AccessControl
# from app.middlewares.trusted_host import TrustedHostMiddleware
from app.database.conn import postgresql_db
from app.nosql.conn import mongodb
from app.routes import index, files, health, crawl, request  # , books, auth, users

from app.utils.singleton_session import aiohttp_context

# API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.middlewares.token_validator import access_control
from starlette.middleware.base import BaseHTTPMiddleware

from app.odmantic.connect import singleton_mongodb
from app.routes.v2 import v2_router
from app.middlewares.api_error_handler import (
    api_erroer_handler,
    api_logger_A,
    api_logger_b,
)

from app.utils.repeat_crawl import init_repeat_crawl

app_name = "isbnapi"


def create_app() -> FastAPI:
    """fastapi 앱을 만드는 함수

    :return: 설정된 FastAPI app
    """
    app = FastAPI()
    # postgresql_db.init_sqlalchemy(
    #     app=app,
    #     dsn=settings.postgresql_dsn,
    #     echo=False,
    # )
    singleton_mongodb.attach_event(app)
    mongodb.init_motor(
        app=app,
        dsn=settings.mongodb_dsn,
    )
    aiohttp_context.init_aiohttp(app=app)
    """미들웨어의 경우, 가장 먼저 add 하는 미들웨어가 view 함수와 근접한다.
    즉 나중에 붙이는 미들웨어가 제일 먼저 반응하므로, CORS를 최 하단에 위치하게 하자.
    """
    # app.add_middleware(
    #     AccessControl,
    #     except_path_list=settings.AUTHORIZATION_EXCEPT_ENDPOINT_LIST,
    #     except_path_regex=settings.AUTHORIZATION_EXCEPT_ENDPOINT_REGEX,
    # )
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=api_erroer_handler)
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origin,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # app.add_middleware(
    #     TrustedHostMiddleware,
    #     allowed_hosts=["*"],
    #     except_path=settings.AUTHORIZATION_EXCEPT_ENDPOINT_LIST,
    # )
    # routes
    app.include_router(v2_router)
    # app.include_router(index.router)
    # app.include_router(files.router)
    # app.include_router(health.router)
    # app.include_router(crawl.router)
    # app.include_router(request.router)
    # app.include_router(books.router, tags=["books", "api"], prefix="/api/v1/books")
    # app.include_router(
    #     auth.router,
    #     tags=["Authentication"],
    #     prefix="/api/v1",
    # )
    # app.include_router(
    #     users.router,
    #     tags=["Users"],
    #     prefix="/api/v1",
    #     dependencies=Depends(API_KEY_HEADER),
    # )
    init_repeat_crawl(app)
    return app


from app.utils.logger import dict_config
import logging

from logging.config import dictConfig

dictConfig(dict_config)
mylogger = logging.getLogger("isbnapi")

app = create_app()

if __name__ == "__main__":
    """
    1. python -m app.main
    2. uvicorn app.main:app --reload

    1번 방식으로 진행할 때 작동하는 코드.
    """
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True,
        log_level="debug",
    )
