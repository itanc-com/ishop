from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), index=True, nullable=True, default=None)
    title = Column(String(255), index=True)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

    parent = relationship("Category", remote_side=[id], backref="children")
