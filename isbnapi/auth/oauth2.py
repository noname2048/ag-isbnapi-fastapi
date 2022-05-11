from http.client import HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta, datetime
from jose import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db import db_user
from jose.exceptions import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "6d436668c3706d392ed8c1bce83995dd04dea3c60b47517b4ca2f7fef7b8173f"
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # 1. 얕은복사를 하는 이유? (깊은복사해도 상관없을듯? - 단순히 복사를 위함)
    # 2. 얕은 복사란? mutable object 제외 복사
    # 3. 여기서 mutable 이라고 할만한게 있나?
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp", expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# excepton for get_current_user
credential_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credetials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise credential_exception

    username = payload.get("username")
    if not username:
        raise credential_exception

    user = db_user.get_user_by_username(db, username)
    return user
