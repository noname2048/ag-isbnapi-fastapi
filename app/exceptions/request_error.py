from starlette import status
from app.exceptions import APIException, APIExceptionV2


class RequestException(APIExceptionV2):
    """
    다른 exception 과 차이를 두기위한 자신만의 exception
    이 에러는 메세지를 표기하고, response로 유저에게 표시할 문구를 가져야한다.
    """

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="undefined",
            description="undefined",
        )


class RequestExsist(RequestException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="request exist",
            description="이미 해당하는 리퀘스트가 존재합니다. 업데이트를 하려면 플래그를 달아주세요",
        )


class RequeustFileTooBig(RequestException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            msg="리퀘스트를 요청하는 csv 파일이 너무 큽니다.",
        )
