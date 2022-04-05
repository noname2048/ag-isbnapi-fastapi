from app.exceptions import APIExceptionV2


class UserError(APIExceptionV2):
    def __init__(self):
        super().__init__(
            status_code=404,
            msg="user error",
            str="no description",
        )


class EmailOrPasswordNotMatch(UserError):
    def __init__(self):
        super()
        """이런식으로 작성하면 다중상속에 불편함이 생기는디."""
