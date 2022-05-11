from venv import create
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db import db_user
from isbnapi.db.models import DbUser
from isbnapi.db.hashing import Hash
from isbnapi.auth.oauth2 import create_access_token

router = APIRouter(tags=["authentication"])


@router.post("/token")
async def get_token(
    request: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # user = db_user.get_user_by_username(request.username)
    user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_UNAUTHORIZED,
            detail="Check username and password",
        )
    if not Hash.verify(user.password, request.password):
        raise HTTPException(
            status_code=status.HTTP_400_UNAUTHORIZED,
            detail="Check username and password",
        )
    payload = {"username": user.username}
    access_token = create_access_token(payload)
    return {"access_token": access_token, "token_type": "Bearer"}
