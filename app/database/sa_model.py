"""
sqlalchemy models (likes schema)

두가지 종류의 모델이 있는데, sql에서 사용하는 sqlalchemy model,
비즈니스 로직으로 사용되는 pydantic 모델. 여기서 pydantic model을 말합니다.
"""
from operator import index
from typing import Counter
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from app.database.conn import Base


class RequestRecord(Base):
    __tablename__ = "request_records"
    id = Column(
        Integer,
        primary_key=True,
    )
    created_at = Column(
        DateTime,
        default=func.utc_timestamp(),
        nullable=False,
    )
    isbn = Column(
        String(13),
        nullable=False,
    )
    status = Column(
        Enum("Accepted", "Ok", "InternalError", "RemoteError", name="status_type"),
        default="Accepted",
        nullable=False,
    )
    detail = Column(
        String(30),
        nullable=True,
    )
    updated_at = Column(
        DateTime,
        default=func.utc_timestamp(),
        onupdate=sa.func.utc_timestamp(),
        nullable=False,
    )
