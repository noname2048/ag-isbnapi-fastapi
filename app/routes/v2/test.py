from typing import Optional
from fastapi import APIRouter, Body

# import logging
# from app.main import mylogger
from app.utils.logger import mylogger
import logging
from pydantic import BaseModel

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn: str = Body("")):
    return {"isbn": isbn}


class Request(BaseModel):
    isbn: str
    update: Optional[str]


@router.post("/test/echo")
async def echo_text(isbn: Request):
    mylogger.info(f"+{isbn}+")
    return {"isbn": isbn}
