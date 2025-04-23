from enum import Enum

from sqlalchemy import Column, DateTime, Integer, String, Text, func
from sqlalchemy import Enum as SQLAlchemyEnum

from db.base import Base


class UserRole(Enum):
    USER = 0
    ADMIN = 1


class UserStatus(Enum):
    DEACTIVE = 0
    ACTIVE = 1
    VERIFIED = 3
    SUSPEND = 4


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(Text, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    picture = Column(Text, nullable=True)
    role = Column(SQLAlchemyEnum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(SQLAlchemyEnum(UserStatus), default=UserStatus.DEACTIVE, nullable=False)
    phone = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
