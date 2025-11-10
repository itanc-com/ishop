from common.http_response.error_response import ErrorCodes

from app.common.exceptions.app_exceptions import InternalServerException
from app.modules.product.repository_interface import ProductRepositoryInterface


class ProductSkuExists:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, sku: str) -> bool:
        try:
            return await self.product_repository.exists_by_field("sku", sku)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to check if product SKU exists",
                data={"sku": sku},
            ) from e
