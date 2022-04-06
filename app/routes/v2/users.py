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


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/users/item")
async def read_item(token: str = Depends(oauth2_scheme)):
    return {"token": token}
