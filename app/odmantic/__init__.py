from starlette import status
from http.client import HTTPException
from .connect import singleton_mongodb


def get_engine():
    if singleton_mongodb.engine is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot connect with internal DB",
        )

    return singleton_mongodb.engine
