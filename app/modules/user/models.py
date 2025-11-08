from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(Text, unique=True, index=True, nullable=False)
    password = Column(Text, nullable=False)
    picture = Column(Text, nullable=True)
    role = Column(Integer, default=2, nullable=False)
    status = Column(Integer, default=0, nullable=False)
    phone = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
