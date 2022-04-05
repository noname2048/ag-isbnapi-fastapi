from starlette import status


class APIExceptionBase(Exception):
    """
    APIException -> APIExceptionV2 -> APIExceptionBase 로 진화
    전버전에서 다중상속에서 어려움이 발생해서 속성으로 사용하도록 변경
    """

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    eng_msg: str
    description: str
    category: str

    def __init__(self):
        if not (self.eng_msg and self.description and self.category):
            raise NotImplementedError(msg="APIExceptionBase: Not implement completely")


class ExampleCategoryAPIException(APIExceptionBase):
    category: str = "Example"


class DetailAPIException(ExampleCategoryAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    eng_msg = "not match"
    description = "email or password not matched"
