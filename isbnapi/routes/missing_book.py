from typing import List, Union
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from isbnapi.db.database import get_db
from isbnapi.schemas import MissingBookBase, MissingBookDisplay, MissingBookFailDisplay
from isbnapi.db import db_missingbook

router = APIRouter(prefix="/missing/book", tags=["missingbook"])

# Create a missing book
@router.post("", response_model=List[Union[MissingBookDisplay, MissingBookFailDisplay]])
async def create_missingbook(
    requests: List[MissingBookBase], db: Session = Depends(get_db)
):
    objs = [db_missingbook.create_missingbook(db, request) for request in requests]
    return objs


# Read all missing books
@router.get("s", response_model=List[MissingBookDisplay])
async def get_all_missing_books(db: Session = Depends(get_db)):
    return db_missingbook.get_all_missingbooks()
