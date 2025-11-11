from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface


class RemoveItemFromCart:
    def __init__(self, cart_repository: CartRepositoryInterface) -> None:
        self.cart_repository = cart_repository

    async def execute(self, user_id: int, product_id: int) -> None:
        try:
            item = await self.cart_repository.get_item(user_id, product_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message=str(e),
                data={"user_id": user_id, "product_id": product_id},
            )

        if not item:
            raise NotFoundException(
                data={"user_id": user_id, "product_id": product_id},
                message=f"Item {product_id} for user with Id {user_id} is not found",
            )

        try:
            await self.cart_repository.delete(user_id=user_id, product_id=product_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to remove item from cart",
                data={"user_id": user_id, "product_id": product_id},
            ) from e
