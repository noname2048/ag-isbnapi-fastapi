from lib2to3.pgen2 import token
from typing import Optional
from datetime import datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import models
from app.common.consts import JWT_SECRET, JWT_ALGORITHM
from app.database.conn import db
from app.database.schema import Users
from app.models import SnsType, Token, UserToken


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


def is_email_exist(email: str) -> bool:
    get_email = Users.get(email=email)
    if get_email:
        return True
    return False


def create_access_token(*, data: dict = None, expires_delta: int = 1) -> str:
    to_encode = data.copy()
    if expires_delta:
        to_encode.update({"exp": datetime.utcnow() + timedelta(hours=expires_delta)})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


@router.post("/register/{sns_type}", status_code=200, response_model=Token)
async def register(
    sns_type: SnsType,
    reg_info: models.UserRegister,
    session: Session = Depends(db.session),
):
    if sns_type == SnsType.email:
        is_exist = await is_email_exist(reg_info.email)
        if not reg_info.email or not reg_info.pw:
            return JSONResponse(
                status_code=400, content=dict(msg="Email and PW must be provided")
            )
        if is_exist:
            return JSONResponse(status_code=400, content=dict(msg="EMAIL_EXISTS"))

        hash_pw = bcrypt.hashpw(
            reg_info.pw.encode("utf-8"), bcrypt.gensalt()
        )  ## TODO: gensalt not saved. is ok?
        new_user = Users.create(
            session, auto_commit=True, pw=hash_pw, email=reg_info.email
        )
        token = dict(
            Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(new_user).dict(exclude={'pw', 'marketing_agree'}))}"
        )
        return token

    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


@router.post("/login/{sns_type}", status_code=200, response_model=Token)
async def login(sns_type: SnsType, user_info: models.UserRegister):
    if sns_type == SnsType.email:
        is_exist = is_email_exist(user_info.email)
        if not user_info.email or not user_info.pw:
            return JSONResponse(
                status_code=400, content=dict(msg="Email and PW must be provided")
            )
        if not is_exist:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        user = Users.get(email=user_info.email)
        is_verified = bcrypt.checkpw(
            user_info.pw.encode("utf-8"), user.pw.encode("utf-8")
        )
        if not is_verified:
            return JSONResponse(status_code=400, content=dict(msg="NO_MATCH_USER"))
        token = dict(
            Authorization=f"Bearer {create_access_token(data=UserToken.from_orm(user).dict(exclude={'pw', 'marketing_agree'}))}"
        )
        return token
    return JSONResponse(status_code=400, content=dict(msg="NOT_SUPPORTED"))


@router.post("/signup", tags=["auth", "signup"])
async def signup(user_id, user_passwd, passwd_confirm):
    if user_passwd == passwd_confirm:
        hashed_passwd = bcrypt.hashpw(user_passwd.encode("utf-8"), bcrypt.gensalt())


@router.post("/login", tags=["auth", "login"])
async def login(user_id, user_passwd):
    db_password = ...
    hashed_passwd = bcrypt.checkpw(user_passwd.encode("utf-8"), db_password)
