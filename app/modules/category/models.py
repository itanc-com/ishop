from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.date_time import get_current_utc


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), index=True, default=0)
    title = Column(String(255), index=True)
    date_created = Column(DateTime, default=get_current_utc, nullable=False)
    date_modified = Column(DateTime, default=get_current_utc, onupdate=get_current_utc, nullable=False)

    parent = relationship("Category", remote_side=[id], backref="children")
