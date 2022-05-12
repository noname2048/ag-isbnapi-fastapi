from typing import List
from fastapi import APIRouter, Depends
from isbnapi.schemas import UserDisplay, UserBase
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db import db_user
from isbnapi.auth.oauth2 import get_current_user
from isbnapi.db.models import DbUser

router = APIRouter(prefix="/user", tags=["user"])

# Create user
@router.post("", response_model=UserDisplay)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Get Current User
@router.get("", response_model=UserDisplay)
async def get_current_user(current_user: DbUser = Depends(get_current_user)):
    return current_user


# Read all users
@router.get("s", response_model=List[UserDisplay])
async def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read user by id
@router.get("/id/{user_id}", response_model=UserDisplay)
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    return db_user.get_user_by_id(db, user_id)


# Read user by username
@router.get("/username/{username}", response_model=UserDisplay)
async def get_user_by_username(
    username: str,
    db: Session = Depends(get_db),
):
    return db_user.get_user_by_username(db, username)


# Read user by email
@router.get("/email/{email}", response_model=UserDisplay)
async def get_user_by_email(
    email: str,
    db: Session = Depends(get_db),
):
    return db_user.get_user_by_email(db, email)
