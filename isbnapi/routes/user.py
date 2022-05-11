from fastapi import APIRouter, Depends
from isbnapi.schemas import UserDisplay, UserBase
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db import db_user

router = APIRouter(prefix="/user", tags=["user"])

# Create user
@router.post("/", response_model=UserDisplay)
async def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)


# Read all users
@router.get("/", response_model=UserDisplay)
async def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)


# Read user by id
@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    return db_user.get_user_by_id(db, user_id)
