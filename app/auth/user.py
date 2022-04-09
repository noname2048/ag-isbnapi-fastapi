from typing import Optional
from pydantic import BaseModel

from http.client import HTTPException
from starlette import status

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError

from app.routes.v2.users import ALGORITHM, TEST_SECRET_KEY


class TokenData(BaseModel):
    email: Optional[str] = None


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 함수안에서 새로이 인스턴스를 만드는 이유는?
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.encode(token, TEST_SECRET_KEY, algorithm=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:  # JWTError 란?
        raise credentials_exception
    # user = get_user()
    user = None
    if user is None:
        raise credentials_exception
    return user
