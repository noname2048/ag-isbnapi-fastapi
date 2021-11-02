from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .engine import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class BookRequest(Base):
    __tablename__ = "bookrequests"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(Integer, index=True)
    date = Column(DateTime)
