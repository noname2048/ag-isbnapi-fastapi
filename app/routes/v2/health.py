from datetime import datetime, timedelta
from fastapi import APIRouter, Response, HTTPException

router = APIRouter()


@router.get("/health/server")
async def server_health():
    current_time = datetime.utcnow()
    kst = current_time + timedelta(hours=9)
    return Response(f"ISBN API" f"\n(KST: {kst.strftime('%Y.%m.%d %H:%M:%S +0900')}")


@router.get("/health/mongodb")
async def mongodb_health():
    raise HTTPException(status_code=404, detail="not implemented")
    # TODO: return mongodb memeory usage
