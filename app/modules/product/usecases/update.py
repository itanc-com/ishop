from common.http_response.error_response import ErrorCodes

from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductInUpdate, ProductOutRead


class ProductUpdate:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int, product_update: ProductInUpdate) -> ProductOutRead:
        try:
            product = await self.product_repository.update_by_id(product_id, product_update)
            if not product:
                raise NotFoundException(
                    data={"product_id": product_id},
                    message="Product not found",
                )
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to update product",
                data={"product_id": product_id, "product_update": product_update.model_dump()},
            ) from e

        return ProductOutRead.model_validate(product)
