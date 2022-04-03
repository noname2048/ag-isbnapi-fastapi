from aiohttp import request
from fastapi import APIRouter
from app.routes.v2 import (
    health,
    books,
    requests,
    test,
    responses,
    users,
)

v2_router = APIRouter()
v2_router.include_router(health.router)
v2_router.include_router(books.router)
v2_router.include_router(requests.router)

v2_router.include_router(test.router)
v2_router.include_router(responses.router)
v2_router.include_router(users.router)
