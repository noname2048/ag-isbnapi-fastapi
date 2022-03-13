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
        ex: Exception = None
    ):
        self.status_code = status_code
        self.msg = msg
        self.ex = ex
        super().__init__(ex)
