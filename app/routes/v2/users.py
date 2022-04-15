from http.client import HTTPException
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from odmantic import AIOEngine
from pydantic.types import SecretStr

from app.exceptions.user_errors import EmailOrPasswordNotMatch
from app.odmantic.connect import singleton_mongodb
from app.odmantic import get_engine
from app.odmantic.models import User
from app.auth.user import get_current_user
from app.auth.password import verify_password, hash_password_with_salt
from app.auth.token import create_access_token
from app.auth import authenticate_user

router = APIRouter()


@router.post("/user/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    engine: AIOEngine = Depends(get_engine),
):
    email = form_data.username
    user = await engine.find_one(User, User.email == email)
    if not user:
        raise EmailOrPasswordNotMatch
    if authenticate_user(email, form_data.password):
        raise EmailOrPasswordNotMatch
    return {"access_token": create_access_token({"email": email})}


@router.get("/users/me", response_model=User)
async def identify_self(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users")
async def list_users(engine: AIOEngine = Depends(get_engine)):
    users = await engine.find(User, limit=100)
    return users


@router.post("/users")
async def make_user(
    email1: str,
    email2: str,
    password1: SecretStr,
    password2: SecretStr,
    engine: AIOEngine = Depends(get_engine),
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
