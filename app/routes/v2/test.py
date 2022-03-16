from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/test/echo")
async def echo_test(isbn=Body(None)):
    return isbn


@router.post("/test/echo")
async def echo_text(isbn=Body(None)):
    return isbn
