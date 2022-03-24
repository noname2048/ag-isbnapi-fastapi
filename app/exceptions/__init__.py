from starlette import status


class APIException(Exception):
    status_code: int
    msg: str
    detail: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        msg: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.msg = msg
        self.ex = ex
        super().__init__(ex)


class APIExceptionV2(Exception):
    """msg로 짤막한 영어상태를, description으로 자세한 한글 풀이를 담을예정"""

    status_code: int
    msg: str
    description: str

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        msg: str = "undefined",
        description: str = "undefined",
    ):
        self.status_code = status_code
        self.msg = msg
        self.description = description
        super().__init__()
