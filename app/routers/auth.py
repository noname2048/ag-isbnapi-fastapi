from typing import Optional
from fastapi import APIRouter, Query

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"],
    responses={
        200: {"description": "Ok"},
        201: {"description": "creation"},
        400: {"description": "Bad Request"},
        404: {"description": "Not found"},
    },
)
import bcrypt


@router.post("/signup", tags=["auth", "signup"])
async def signup(user_id, user_passwd, passwd_confirm):
    if user_passwd == passwd_confirm:
        hashed_passwd = bcrypt.hashpw(user_passwd.encode("utf-8"), bcrypt.gensalt())


@router.post("/login", tags=["auth", "login"])
async def login(user_id, user_passwd):
    db_password = ...
    hashed_passwd = bcrypt.checkpw(user_passwd.encode("utf-8"), db_password)
