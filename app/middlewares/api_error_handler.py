from fastapi import FastAPI, middleware, Request
from fastapi.responses import JSONResponse
import time

from app.exceptions import APIException, APIExceptionV2
from app.exceptions.request_error import RequestException
from app.exceptions.base import APIExceptionBase

from app.utils.logger import mylogger


async def api_erroer_handler(request: Request, call_next):
    """API에러가 레이즈될경우 처리하는 미들웨어"""
    try:
        response = await call_next(request)
        return response

    except RequestException as r_exception:
        mylogger.warn(f"request exception - {r_exception.msg}")
        response = JSONResponse(
            content={
                "msg": r_exception.msg,
                "description": r_exception.description,
            },
            status_code=r_exception.status_code,
        )
        return response

    except APIExceptionV2 as api_exception:
        mylogger.warn(f"capture exceptionv2 - {api_exception.msg}")
        response = JSONResponse(
            content={
                "msg": api_exception.msg,
                "description": api_exception.description,
            },
            status_code=api_exception.status_code,
        )
        return response

    except APIException as api_exception:
        mylogger.warn(f"capture error - {api_exception.msg}")
        response = JSONResponse(
            content={"msg": api_exception.msg},
            status_code=api_exception.status_code,
        )
        return response

    except APIExceptionBase as api_exception:
        mylogger.warn(f"capture error - {api_exception.msg}")
        resposne = JSONResponse(
            content={
                "msg": api_exception.eng_msg,
            },
            status_code=api_exception.status_code,
        )


async def api_logger_A(request: Request, call_next):
    mylogger.info("A-")
    response = await call_next(request)
    mylogger.info("-A")
    return response


async def api_logger_b(request: Request, call_next):
    mylogger.info("B-")
    response = await call_next(request)
    mylogger.info("-B")
    return response
