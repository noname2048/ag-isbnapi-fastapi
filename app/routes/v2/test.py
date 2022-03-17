from fastapi import APIRouter, Body

# import logging
# from app.main import mylogger
from app.utils.logger import mylogger
import logging

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn: str = Body("")):
    return {"isbn": isbn}


@router.post("/test/echo")
async def echo_text(isbn: str = Body("")):
    isbn: str = isbn.rstrip('"')
    mylogger.info(f"+{isbn}+")
    return {"isbn": int(isbn)}
