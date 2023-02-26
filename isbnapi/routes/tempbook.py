from fastapi import APIRouter, Path, Depends, HTTPException, status
from isbnapi.schemas import TempBookDisplay
import re
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.db.models import DbTempBook
from typing import List


router = APIRouter(prefix="tempbook", tags=["tempbook"])
isbn_pattern = re.compile(r"^[0-9]{13}$")


@router.get("s/{isbn}", response_model=TempBookDisplay)
async def get_tempbook_by_isbn(
    isbn: Path(regex=r"^[0-9]{13}"), db: Session = Depends(get_db)
):
    tempbook = db.query(DbTempBook).filter(DbTempBook.isbn == isbn).first()
    if not tempbook:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tempbook with isbn {isbn} not found",
        )

    return tempbook


@router.get("s", response_model=List[TempBookDisplay])
async def get_all_tempbook(db: Session = Depends(get_db)):
    tempbooks = db.query(DbTempBook).all()
    return tempbooks
