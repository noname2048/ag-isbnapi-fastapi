from datetime import datetime, timedelta

from fastapi import APIRouter

router = APIRouter()


@router.post("/auth/google/login")
async def signup():
    pass
