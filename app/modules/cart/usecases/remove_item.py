from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.cart.repository_interface import CartItemRepositoryInterface


class RemoveItemFromCart:
    def __init__(self, cart_item_repository: CartItemRepositoryInterface) -> None:
        self.cart_item_repository = cart_item_repository

    async def execute(self, user_id: int, product_id: int) -> None:
        try:
            item = await self.cart_item_repository.get_by_user_and_product(user_id, product_id)
        except SQLAlchemyError as e:
            raise DatabaseOperationException(
                operation="read",
                message=str(e),
                data={"user_id": user_id, "product_id": product_id},
            )

        if not item:
            raise EntityNotFoundException(
                data={"user_id": user_id, "product_id": product_id},
                message=f"CartItem with user_id={user_id} and product_id={product_id} not found",
            )

        try:
            await self.cart_item_repository.remove(user_id=user_id, product_id=product_id)
        except IntegrityError as e:
            await self.cart_item_repository.session.rollback()
            raise DatabaseOperationException(
                operation="delete",
                message=f"Integrity violation: {str(e)}",
                data={"user_id": user_id, "product_id": product_id},
            )
        except SQLAlchemyError as e:
            await self.cart_item_repository.session.rollback()
            raise DatabaseOperationException(
                operation="delete",
                message=str(e),
                data={"user_id": user_id, "product_id": product_id},
            )
