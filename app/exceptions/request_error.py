from starlette import status
from app.exceptions import APIException, APIExceptionV2


class RequestExsist(APIExceptionV2):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="request exist",
            description="이미 해당하는 리퀘스트가 존재합니다. 업데이트를 하려면 플래그를 달아주세요",
        )


class RequeustFileTooBig(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            msg="리퀘스트를 요청하는 csv 파일이 너무 큽니다.",
        )
