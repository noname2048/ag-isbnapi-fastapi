from http.client import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.auth.password import hash_password_with_salt, verify_password
from app.auth.user import get_user
from odmantic import AIOEngine


async def authenticate_user(email: str, password: str):
    user = await get_user(email)
    if not user:
        return False

    hashed_password = hash_password_with_salt(password, user.salt)
    if not verify_password(hashed_password, user.hashed_password):
        return False

    return True
