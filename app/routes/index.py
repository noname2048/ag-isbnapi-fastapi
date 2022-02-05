from datetime import datetime

from fastapi import APIRouter, Depends, Request, Response as R
from starlette.responses import Response

router = APIRouter()


@router.get("/")
async def index():
    current_time = datetime.utcnow()
    return Response(f"ISBN API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}")
    return R(
        content=f"ISBN API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}",
        status_code=200,
    )


@router.get("/health")
async def health(request: Request):
    """
    상태 체크용 API

    :return:
    """
    print("state.user", request.state.user)
    current_time = datetime.utcnow()
    return Response(f"ISBN API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}")
    return R(
        content=f"ISBN API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}",
        status_code=200,
    )
