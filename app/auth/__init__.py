from http.client import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.odmantic import get_engine
from app.auth.password import hash_password_with_salt, verify_password
from app.auth.user import get_user


engine = get_engine()


async def authenticate_user(email, password):
    user = await get_user(email)
    if not user:
        return False

    hashed_password = hash_password_with_salt(password, user.salt)
    if not verify_password(hashed_password, user.hashed_password):
        return False

    return True
