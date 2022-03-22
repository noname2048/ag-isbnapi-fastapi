from fastapi import FastAPI, middleware, Request, Response
import time

from app.exceptions import APIException


async def api_erroer_handler(request: Request, call_next):
    """API에러가 레이즈될경우 처리하는 미들웨어"""
    try:
        response = await call_next(request)
    except APIException as api_exception:
        api_exception.detail
        api_exception.msg
        api_error = {"detail": api_exception.detail, "msg": api_exception.msg}
        return Response({"error": api_error}, status_code=api_exception.status_code)

    return response
