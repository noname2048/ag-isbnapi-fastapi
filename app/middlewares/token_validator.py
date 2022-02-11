import time
import typing
import jwt
import re

from fastapi.params import Header
from jwt import PyJWTError
from pydantic import BaseModel
from starlette.requests import Request
from starlette.datastructures import URL, Headers
from starlette.responses import JSONResponse
from starlette.responses import PlainTextResponse, RedirectResponse, Response
from starlette.types import ASGIApp, Receive, Scope, Send

from app.common import config, consts
from app.models import UserToken

from app.utils.date_utils import Delta

from datetime import datetime
from fastapi import FastAPI, Request

import logging

from fastapi.logger import logger

# logger = logging.getLogger("fastapi")
# logger.setLevel(logging.DEBUG)


async def access_control(request: Request, call_next):
    request.state.req_time = datetime.utcnow()
    request.state.user = None
    request.state.inspect = None
    ip = request.headers.get("x-forwarded-for", request.client.host)
    if "," in ip:
        ip = ip.split(",")[0]
    request.state.ip = ip
    logger.info("request.state.ip")
    logger.info("hi")

    response = await call_next(request)
    return response


class AccessControl:
    def __init__(
        self,
        app: ASGIApp,
        except_path_list: typing.Sequence[str] = None,
        except_path_regex: str = None,
    ) -> None:
        if except_path_list is None:
            except_path_list = ["*"]
        self.app = app
        self.except_path_list = except_path_list
        self.except_path_regex = except_path_regex

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        print(self.except_path_regex)
        print(self.except_path_list)

        request = Request(scope=scope)
        headers = Headers(scope=scope)

        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.is_admin_access = None
        request.state.ip_from = (
            request.headers["x-forwarded-for"]
            if "x-forwarded-for" in request.headers.keys()
            else None
        )

        # Authorization Passed (ignored)
        if (
            self.url_pattern_check(request.url.path, self.except_path_regex)
            or request.url.path in self.except_path_list
        ):
            return await self.app(scope, receive, send)

        AUTHORIZATION = "Authorization"
        if request.url.path.startswith("/api"):

            if AUTHORIZATION not in request.headers.keys():
                response = JSONResponse(
                    status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED")
                )
                return await response(scope, receive, send)

            request.state.user = self.token_decode(
                access_token=request.headers.get(AUTHORIZATION)
            )
        else:
            print(request.cookies)

            if AUTHORIZATION not in request.cookies.keys():
                response = JSONResponse(
                    status_code=401, content=dict(msg="AUTHORIZATION_REQUIRED")
                )
                return await response(scope, receive, send)

            request.state.user = self.token_decode(
                access_token=request.cookies.get(AUTHORIZATION)
            )

        request.state.req_time = Delta.datetime_after_hours()
        print(Delta.datetime_after_hours())
        print(Delta.date())
        print(Delta.date_num())

        print(request.cookies)
        print(headers)
        res = await self.app(scope, receive, send)
        return res

    @staticmethod
    def url_pattern_check(path, pattern):
        result = re.match(pattern, path)
        if result:
            return True
        return False

    @staticmethod
    def token_decode(access_token):
        try:
            access_token = access_token.replace("Bearer ", "")
            payload = jwt.decode(
                access_token, key=consts.JWT_SECRET, algorithms=[consts.JWT_ALGORITHM]
            )
        except PyJWTError as e:
            print(e)
            # TODO: raise Error
        return payload
