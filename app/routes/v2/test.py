from fastapi import APIRouter, Body

# import logging
# from app.main import mylogger
from app.utils.logger import mylogger

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn: str = Body("")):
    mylogger.warning(isbn)
    return {"isbn": isbn}


@router.post("/test/echo")
async def echo_text(isbn: str = Body("")):
    return {"isbn": isbn}
