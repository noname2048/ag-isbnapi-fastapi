from starlette import status

from app.exceptions import APIException

class MongoObjectNotFound(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="몽고 object를 찾을 수 없습니다",
        )

class AladinResponseError(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="알라딘에서 isbn13 으로 정보를 조회하였으나, 응답이 200이 아닙니다",
        )

class IsbnPatternError(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="mongo object에 저장된 isbn 형식이 이상합니다",
        )

class AladinJsonDecodeFail(APIException):
    def __init__(self, ex: Exception = None)다
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="알라딘에서 정보를 파싱하는데에 있어 json 디코드 에러가 발생하였습니다",
        )


class AladinItemNotFound(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            msg="알라딘에서 json 정보를 뽑아내었지만, item은 찾지 못했습니다",
        )
