from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


# pydantic models
class Request(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    isbn13: int
    created_at: datetime
    response_id: str
