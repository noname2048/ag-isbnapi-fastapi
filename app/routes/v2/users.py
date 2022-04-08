from doctest import FAIL_FAST
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic.types import SecretStr

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import User

router = APIRouter()


@router.get("/users")
async def list_users():
    engine = singleton_mongodb.engine
    users = await engine.find(User, limit=100)
    return users


@router.post("/users")
async def make_user(
    email1: str, email2: str, password1: SecretStr, password2: SecretStr
):
    if email1 != email2 or password1 != password2:
        pass
    engine = singleton_mongodb.engine
    user = User(email=email1, password=password1)
    await engine.save(user)
    return user


@router.get("/user")
async def show_me():
    """유저의 마이페이지 (비번수정등)"""
    pass


"""
Depends 는 __call__속성을 가진 Object를 통해 발현가능
Header 에서 Authoriztion 속성을 가져온다 (scheme와 param)
scheme가 bearer이어야 한다. (raise 401)
정상적일경우 param을 리턴한다.
"""
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/item")
async def read_item(token: str = Depends(oauth2_scheme)):
    return {"token": token}


TEST_SECRET_KEY = "b878d60ae6e11afc2cd07cf7b9a64eb3cdd00055130e60f72b4f8d924304c406"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPRIE_MINUTES = 30

from typing import Optional
from pydantic import BaseModel
import os
import binascii
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


def make_password(password) -> str:
    salt = os.urandom(15)
    salt = binascii.b2a_hex(salt)
    result = hash_password(f"{password}_{salt}")
    return result, salt


def hash_password(password) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email, password):
    engine = singleton_mongodb.engine
    user = await engine.find_one(User, User.email == email)
    if not user:
        return False
    salt = user.salt
    auth = verify_password(f"{password}_{salt}", user.password)
    if not auth:
        return False

    return True
