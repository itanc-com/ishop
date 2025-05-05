from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    sku = Column(Text, unique=True, nullable=False)
    is_available = Column(Boolean, default=False)
    price = Column(Numeric(15, 2), nullable=False)
    is_visible = Column(Boolean, default=False)
    date_created = Column(DateTime, default=func.now())
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now())

    category = relationship("Category", backref="products")
