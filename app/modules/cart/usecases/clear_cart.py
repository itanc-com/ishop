from app.common.exceptions.app_exceptions import InternalServerException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface


class ClearCart:
    def __init__(self, cart_repository: CartRepositoryInterface) -> None:
        self.cart_repository = cart_repository

    async def execute(self, user_id: int) -> None:
        try:
            await self.cart_repository.delete_all_items(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to clear cart items",
                data={"user_id": user_id},
            ) from e
