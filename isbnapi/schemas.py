from pydantic import BaseModel, EmailStr, SecretStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: SecretStr


class UserDisplay(BaseModel):
    username: str
    email: EmailStr

    class Config:
        orm_mode = True
