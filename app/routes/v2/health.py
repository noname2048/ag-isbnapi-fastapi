from datetime import datetime, timedelta
from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health/server")
async def server_health():
    current_time = datetime.utcnow()
    kst = current_time + timedelta(hours=9)
    return Response(f"ISBN API" f"\n(KST: {kst.strftime('%Y.%m.%d %H:%M:%S +0900')}")
