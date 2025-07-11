from sqlalchemy import Column, DateTime, Float, Integer, func

from app.db.base import Base


class CartItem(Base):
    __tablename__ = "tbl_cart_items"

    user_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    price = Column(Float, default=0, nullable=False)
    total = Column(Integer, default=0, nullable=False)
    date_created = Column(DateTime, default=func.now(), nullable=False)
    date_modified = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
