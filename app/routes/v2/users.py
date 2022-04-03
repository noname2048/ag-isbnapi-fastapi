from doctest import FAIL_FAST
from fastapi import APIRouter

from app.odmantic.connect import singleton_mongodb
from app.odmantic.models import User

router = APIRouter()


@router.get("/users")
async def list_users():
    engine = singleton_mongodb.engine
    users = await engine.find(User, limit=100)
    return users


@router.post("/users")
async def make_user(email: str, password: str):
    engine = singleton_mongodb.engine
    user = User(email=email, password=password)
    await engine.save(user)
    return user
