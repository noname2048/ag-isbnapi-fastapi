from re import S
from xmlrpc.client import boolean
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional, Union, List


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDisplay(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserPatchBase(BaseModel):
    username: Optional[str]
    email: Optional[str]
    password: Optional[str]


class MissingBookBase(BaseModel):
    isbn: str = Field(..., example="1234567890123")


class MissingBookDisplay(BaseModel):
    id: int
    isbn: str = Field(..., regex=r"\d{13}", example="1234567890123")
    timestamp: datetime
    error_message: Optional[str]

    class Config:
        orm_mode = True


class MissingBookFailDisplay(BaseModel):
    isbn: str = Field(..., example="1234567890123")
    detail: str = Field(..., example="Not a unqiue key")

    class Config:
        orm_mode = True


# for request books
class MissingBook(BaseModel):
    id: int
    isbn: str


class BookBase(BaseModel):
    isbn: str
    title: str
    description: str
    cover: str
    cover_type: str
    publisher: str
    price: int
    pub_date: date
    author: str
    missingbook_id: int


class BookDisplayExample(BaseModel):
    isbn: str = Field(..., example="9791188102051")
    title: str = Field(..., example="더 시스템 - 거의 모든 일에 실패하던 자가 결국 큰 성공을 이루어낸 방법")
    description: str = Field(
        ...,
        example="전 세계 65개국 2,000여개 신문사에 실린 세계에서 가장 유명한 만화 ‘딜버트’의 작가 스콧 애덤스. 그는 『더 시스템』을 통해 “성공하려면 열정을 좇으라”는 자기계발서의 진부한 메시지를 뒤엎는다. 무조건 열정을 좇으며 포기하지 않는다고 성공하는 것이 아니며, 오히려 성공이 열정을 불러온다고 반박한다.",
    )
    cover: str = Field(
        ...,
        example="https://image.aladin.co.kr/product/24605/87/cover/k412631174_2.jpg",
    )
    cover_type: str = Field(..., example="absolute")
    publisher: str = Field(..., example="베리북")
    price: int = Field(..., example="16000")
    pub_date: date = Field(..., example="2020-07-16")
    author: str = Field(..., example="스콧 애덤스 지음, 김인수 옮김")


class TempBookBase(BaseModel):
    isbn: str


class TempBookDisplay(BaseModel):
    id: int
    isbn: str
    timestamp: datetime


class BookInfoBase(BaseModel):
    isbn: str = Field(..., example="9791161340463")
    title: str
    description: str
    cover: str
    cover_type: str
    publisher: str
    price: float
    pub_date: date
    author: str


class BookInfoDisplay(BaseModel):
    id: int

    isbn: str = Field(..., example="9791161340463")
    title: str
    description: str
    cover: str
    cover_type: str
    publisher: str
    price: int
    pub_date: date
    author: str

    created_at: date
    updated_at: date

    is_error: bool
    error_msg: Optional[str]

    class Config:
        orm_mode = True


class BookInfoDisplayV2(BaseModel):
    type: str
    error_detail: Union[str, None] = None
    requested_info: Union[TempBookDisplay, None] = None
    info: Union[BookInfoDisplay, None] = None


class BookInfoErrorBase(BaseModel):
    isbn: str
    is_error: bool
    error_msg: str
