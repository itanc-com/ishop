from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer

from app.db.base import Base
from app.utils.date_time import get_current_utc


class CartItem(Base):
    __tablename__ = "cart_items"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, default=0.0, nullable=False)
    subtotal = Column(Float, default=0.0, nullable=False)
    date_created = Column(DateTime, default=get_current_utc, nullable=False)
    date_modified = Column(DateTime, default=get_current_utc, onupdate=get_current_utc, nullable=False)
