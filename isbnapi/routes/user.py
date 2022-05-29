from typing import List
from fastapi import APIRouter, Depends
from isbnapi.schemas import UserDisplay, UserBase, UserPatchBase
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db import db_user
from isbnapi.auth.oauth2 import get_current_user
from isbnapi.db.models import DbUser
from isbnapi.db.hashing import Hash


router = APIRouter(prefix="/user", tags=["user"])

# Get current user
@router.get("", response_model=UserDisplay)
async def get_current_user(current_user: DbUser = Depends(get_current_user)):
    return current_user


# Create user
@router.post("", response_model=UserDisplay)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Get all users
@router.get("s", response_model=List[UserDisplay])
async def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Get user by id
@router.get("s/{id}", response_model=UserDisplay)
async def get_user_by_username(
    id: int,
    db: Session = Depends(get_db),
):
    return db_user.get_user_by_id(db, id)


@router.patch("s/{id}")
async def patch_user(id: int, request: UserPatchBase, db: Session = Depends(get_db)):
    user: DbUser = db_user.get_user_by_id(db, id)
    if request.username:
        user.username = request.username
    if request.password:
        user.password = Hash.bcrypt(request.password)
    if request.email:
        user.email == request.email

    db.commit()
    db.refresh(user)
    return user


@router.delete("s/{id}")
async def delete_user(id, db: Session = Depends(get_db)):
    user = db_user.get_user_by_id(id)
    db.delete(user)
    db.commit()

    return {"Ok"}
