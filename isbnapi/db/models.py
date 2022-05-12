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


class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


class DbMissingBook(Base):
    __tablename__ = "missingbooks"
    id = Column(Integer, primary_key=True, index=True)
    isbn = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)


# for cover_type in DbBook
class CoverType(str, enum.Enum):
    relative = "relative"
    absolute = "absolute"


class DbBook(Base):
    __tablename__ = "books"
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
