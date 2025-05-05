from sqlalchemy.orm import Session

from .models import Product
from .schemas import ProductInsert, ProductUpdate


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: ProductInsert)-> Product:
        product = Product(**data.model_dump())
        self.session.add(product)
        self.session.commit()
        self.session.refresh(product)
        return product

    def get_by_id(self, product_id: int) -> Product | None:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def list_all(self) -> list[Product]:
        return self.session.query(Product).all()

    def delete(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()

    def update(self, product: Product, data: ProductUpdate) -> Product:
        for key, value in vars(data).items():
            setattr(product, key, value)
        self.session.commit()
        self.session.refresh(product)
        return product
