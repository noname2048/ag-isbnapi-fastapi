from isbnapi.db.database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Date,
    Enum,
    ForeignKey,
)
from datetime import datetime
import enum
from sqlalchemy.orm import relationship


class DbUser(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DbMissingBook(Base):
    __tablename__ = "missingbook"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    error_message = Column(String)
    book = relationship("DbBook", back_populates="missingbook")


# for cover_type in DbBook
class CoverType(str, enum.Enum):
    relative = "relative"
    absolute = "absolute"


class DbTempBook(Base):
    __tablename__ = "tempbook"
    id = Column(Integer, primary_key=True)
    isbn = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DbBookInfo(Base):
    __tablename__ = "bookinfo"
    id = Column(Integer, primary_key=True)
    isbn = Column(String, index=True, unique=True, nullable=False)
    title = Column(String, default="")
    description = Column(String, default="")
    cover = Column(String, default="")
    cover_type = Column(Enum(CoverType), default=None)
    publisher = Column(String, default="")
    price = Column(Integer, default=0)
    pub_date = Column(Date, default=None)
    author = Column(String, default="")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    is_error = Column(Boolean, default=False)
    error_msg = Column(String)


class DbBook(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(String)
    cover = Column(String)
    cover_type = Column(Enum(CoverType))
    publisher = Column(String)
    price = Column(Integer)
    pub_date = Column(Date)
    author = Column(String)

    missingbook_id = Column(Integer, ForeignKey("missingbook.id"))
    missingbook = relationship("DbMissingBook", back_populates="book")
