from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)

        return product

    async def update_by_id(self, product_id: int, updated_product: Product) -> Product | None:
        product = await self.session.get(Product, product_id)
        if not product:
            return None

        for attr, value in vars(updated_product).items():
            if attr != "id" and hasattr(product, attr):
                setattr(product, attr, value)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_by_id(self, product_id: int) -> Product | None:
        product = await self.session.get(Product, product_id)

        if not product:
            return None

        await self.session.delete(product)
        await self.session.commit()
        return product

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)

    async def list_all(self, category_id: int | None = None, skip: int = 0, limit: int = 10) -> list[Product]:
        query = select(Product)

        if category_id is not None:
            query = query.where(Product.category_id == category_id)

        query = query.offset(skip).limit(limit)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def exists_by_field(self, field: str, value: Any) -> bool:
        stmt = select(Product).where(getattr(Product, field) == value)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def count_all(self, category_id: int | None = None) -> int:
        """Count total products with optional category filter."""
        query = select(func.count(Product.id))

        if category_id is not None:
            query = query.where(Product.category_id == category_id)

        result = await self.session.execute(query)
        return result.scalar() or 0
