from app.common.exceptions.app_exceptions import DatabaseOperationException
from app.modules.product.repository_interface import ProductRepositoryInterface


class ProductSkuExists:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, sku: str) -> bool:
        try:
            return await self.product_repository.exists_by_field("sku", sku)
        except Exception as e:
            raise DatabaseOperationException(
                operation="exists_by_sku",
                message=str(e),
                data={"sku": sku},
            )
