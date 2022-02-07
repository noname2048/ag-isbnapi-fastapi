from datetime import datetime, timedelta
from dataclasses import asdict

import uvicorn

from fastapi import FastAPI, APIRouter
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware

from app.common.config import get_config
from app.middlewares.token_validator import AccessControl
from app.middlewares.trusted_host import TrustedHostMiddleware
from app.database.conn import db
from app.routes import index  # , books, auth, users


API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


def create_app() -> FastAPI:
    """fastapi 앱을 만드는 함수

    :return: FastAPI app
    """
    # config
    c = get_config()
    conf_dict = asdict(c)
    # app
    app = FastAPI()
    # DB
    # db.init_app(app, **conf_dict)
    # redis
    # middleware
    app.add_middleware(
        AccessControl,
        except_path_list=[],
        except_path_regex="",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=c.ALLOWED_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
        except_path=["/health"],
    )
    # routes
    app.include_router(index.router)
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
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
