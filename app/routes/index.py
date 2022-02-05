from datetime import datetime

from fastapi import APIRouter, Depends, Request
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.database import db
from app.database.schema import Users

router = APIRouter()


@router.get("/")
async def index():
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}"
    )


@router.get("/health")
async def health(request: Request):
    """
    ELB 상태 체크용 API

    :return:
    """
    print("state.user", request.state.user)
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}"
    )
