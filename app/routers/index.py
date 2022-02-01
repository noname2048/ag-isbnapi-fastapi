from datetime import datetime

from fastapi import APIRouter, Depends
from starlette.responses import Response
from sqlalchemy.orm import Session

from app.database import db
from app.database.schema import Users

router = APIRouter()


@router.get("/")
async def index(
    session: Session = Depends(db.session),
):
    """
    ELB 상태 체크용 API

    :return:
    """
    if False:
        user = Users(status="active")
        session.add(user)
        session.commit()

    Users().create(session, auto_commit=True, name="코알라")
    current_time = datetime.utcnow()
    return Response(
        f"Notification API (UTC: {current_time.strftime('%Y.%m.%d %H:%M:%S')}"
    )
