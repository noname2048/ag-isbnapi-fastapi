from re import S
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDisplay(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class MissingBookBase(BaseModel):
    isbn: str = Field(..., example="1234567890123")


class MissingBookDisplay(BaseModel):
    id: int
    isbn: str = Field(..., regex=r"\d{13}", example="1234567890123")
    timestamp: datetime

    class Config:
        orm_mode = True


class MissingBookFailDisplay(BaseModel):
    isbn: str = Field(..., example="1234567890123")
    detail: str = Field(..., example="Not a unqiue key")

    class Config:
        orm_mode = True
