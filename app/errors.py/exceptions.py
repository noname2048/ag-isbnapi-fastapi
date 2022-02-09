"""
ISBN API에 사용될 Exception들을 정의합니다.

추후에 DB에 Exception을 모두 넣어서
서버 시작시 DB에서 Exception을 가져와 실행하는 형태가 된다고 설명.
그러면 class 이름이 동적으로 생성되는데 어디에서 Exception을 import.?
"""
from http import HTTPStatus
from typing import Union


class APIException(Exception):
    status: HTTPStatus
    msg: str
    code: str

    def __init__(
        self,
        *,
        status: Union[int, HTTPStatus],
        msg: str,
        detail: str,
        code: str = "Not Defined",
    ):
        if type(status) is int:
            self.status = HTTPStatus(status)
        else:
            self.status = status
        self.msg = msg
        self.code = code


class NotFoundUserEx(APIException):
    def __init__(self, user_id: int):
        super().__init__(
            status=HTTPStatus(400),
            msg=f"해당 유저를 찾을 수 없습니다.",
            defail=f"Not Found User ID: {user_id}",
            code=f"HTTPStatus",
        )
