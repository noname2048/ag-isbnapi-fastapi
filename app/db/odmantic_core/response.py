from odmantic import Field, Model

from typing import Optional
from datetime import datetime as sys_datetime


class Response(Model):
    isbn13: int
    response_date: sys_datetime
    request_id: str

    class Config:
        collection = "responses"
