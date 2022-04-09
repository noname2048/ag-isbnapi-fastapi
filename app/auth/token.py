from typing import Optional
from datetime import timedelta, datetime
from jose import jwt, JWTError

from app.routes.v2.users import ALGORITHM

# openssl rand -hex 32
SECRET_KEY = "b878d60ae6e11afc2cd07cf7b9a64eb3cdd00055130e60f72b4f8d924304c406"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expire_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expire is None:
        expire = datetime.utcnow() + timedelta(minutes=15)
    else:
        expire = datetime.utcnow() + expire_delta

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
