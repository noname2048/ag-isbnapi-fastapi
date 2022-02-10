from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Request, Response as R
from starlette.responses import Response

router = APIRouter()


@router.get("/")
async def index():
    """
    상태 체크용 API

    :return:
    """
    current_time = datetime.utcnow()
    kst = current_time + timedelta(hours=9)
    return Response(
        f"ISBN API"
        f"\n(UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
        f"\n(KST: {kst.strftime('%Y.%m.%d %H:%M:%S +0900')})"
    )


@router.get("/health")
async def health(request: Request):
    """
    상태 체크용 API

    :return:
    """
    print("state.user", request.state.user)
    current_time = datetime.utcnow()
    kst = current_time + timedelta(hours=9)
    return Response(
        f"ISBN API"
        f"\n(UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')})"
        f"\n(KST: {kst.strftime('%Y.%m.%d %H:%M:%S +0900')})"
    )
