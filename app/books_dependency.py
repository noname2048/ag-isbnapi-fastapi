from fastapi import Query


class PagenationQueryParams:
    def __init__(
        self, limit: int = Query(10, ge=10, le=100), offset: int = Query(0, ge=0)
    ):
        self.limit = limit
        self.offset = offset
