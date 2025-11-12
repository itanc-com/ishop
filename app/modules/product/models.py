from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.utils.date_time import get_current_utc


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    sku = Column(Text, unique=True, nullable=False)
    is_available = Column(Boolean, default=False)
    price = Column(Numeric(15, 2), nullable=False)
    is_visible = Column(Boolean, default=False)
    date_created = Column(DateTime, default=get_current_utc, nullable=False)
    date_modified = Column(DateTime, default=get_current_utc, onupdate=get_current_utc, nullable=False)

    category = relationship("Category", backref="products")
