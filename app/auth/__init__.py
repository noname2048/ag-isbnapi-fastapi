from http.client import HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.odmantic import get_engine


engine = get_engine()
