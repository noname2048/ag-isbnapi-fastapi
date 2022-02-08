from fastapi import APIRouter, Request

from app.database.schema import Users
from app.models import UserMe

router = APIRouter()


@router.get("/me", response_model=UserMe)
async def get_user(request: Request):
    """
    유저정보를 가져오는 API

    :param request:
    :return:
    """
    user = request.state.user
    user_info = Users.get(id=user.id)
    return user_info
