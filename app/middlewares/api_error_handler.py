from fastapi import FastAPI, middleware, Request
from fastapi.responses import JSONResponse
import time

from app.exceptions import APIException


async def api_erroer_handler(request: Request, call_next):
    """API에러가 레이즈될경우 처리하는 미들웨어"""
    try:
        response = await call_next(request)
    except APIException as api_exception:
        api_error = {"msg": api_exception.msg}
        return JSONResponse(
            content={"error": api_error},
            status_code=api_exception.status_code,
        )

    return response
