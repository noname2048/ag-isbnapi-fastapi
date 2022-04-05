from starlette import status
from app.exceptions.base import APIExceptionBase


class UserManagementError(APIExceptionBase):
    category: str = "UserManagementError"


class EmailOrPasswordNotMatch(UserManagementError):
    status_code: str = status.HTTP_400_BAD_REQUEST
    eng_msg: str = "Not matched."
    description: str = "Email or Password not match"
