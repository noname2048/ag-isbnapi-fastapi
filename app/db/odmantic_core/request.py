from odmantic import Field, Model

from typing import Optional
from datetime import datetime as sys_datetime


class Request(Model):
    isbn13: int
    request_date: sys_datetime
    response_code: int
    response_date: Optional[sys_datetime]
    response_id: Optional[str]
    user_id: Optional[int]
    user_info: Optional[str]

    class Config:
        collection = "requests"
