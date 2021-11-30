from pydantic import BaseModel
import datetime

from sqlalchemy.orm import relationship
from app.db.engine import Base

from sqlalchemy import Column, Integer, Datetime, ForeignKey


class BookRequest(Base):
    __tablename__ = "bookrequests"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(Integer, index=True)
    date = Column(Datetime)


class BookResponse(Base):
    __tablename__ = "bookresponses"

    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(Integer, index=True)
    date = Column(Datetime)

    request = Column(Integer, ForeignKey("bookrequests.id"))
    request_id = relationship("bookrequests", back_populates="request")
