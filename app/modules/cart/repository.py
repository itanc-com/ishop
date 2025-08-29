from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException

from .models import CartItem
from .repository_interface import CartItemRepositoryInterface


class CartItemRepository(CartItemRepositoryInterface):
    model_class = CartItem

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, cart_item: CartItem) -> CartItem:
        try:
            self.session.add(cart_item)
            await self.session.commit()
            await self.session.refresh(cart_item)
            return cart_item
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={"user_id": cart_item.user_id, "product_id": cart_item.product_id},
            )

    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        try:
            self.session.add_all(cart_items)
            await self.session.commit()
            for cart_item in cart_items:
                await self.session.refresh(cart_item)
            return cart_items
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="create",
                message=str(e),
                data={"items": [{"user_id": cart_item.user_id, "product_id": cart_item.product_id} for cart_item in cart_items]},
            )

    async def find_all(self, user_id: int) -> list[CartItem]:
        try:
            stmt = select(self.model_class).where(self.model_class.user_id == user_id)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise DatabaseOperationException(operation="read", message=str(e), data={"user_id": user_id})

    async def clear_cart(self, user_id: int) -> None:
        try:
            await self.session.execute(CartItem.__table__.delete().where(CartItem.user_id == user_id))
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseOperationException(operation="delete", message=str(e), data={"user_id": user_id})

    async def get_by_user_and_product(self, user_id: int, product_id: int) -> CartItem | None:
        try:
            stmt = select(self.model_class).where(
                self.model_class.user_id == user_id, self.model_class.product_id == product_id
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            raise DatabaseOperationException(
                operation="read", message=str(e), data={"user_id": user_id, "product_id": product_id}
            )

    async def remove(self, user_id: int, product_id: int) -> None:
        try:
            stmt = select(self.model_class).where(
                self.model_class.user_id == user_id, self.model_class.product_id == product_id
            )
            result = await self.session.execute(stmt)
            cart_item = result.scalar_one_or_none()

            if not cart_item:
                raise EntityNotFoundException(
                    data={"user_id": user_id, "product_id": product_id},
                    message=f"CartItem with user_id={user_id} and product_id={product_id} not found",
                )

            await self.session.delete(cart_item)
            await self.session.commit()

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="delete", message=str(e), data={"user_id": user_id, "product_id": product_id}
            )
