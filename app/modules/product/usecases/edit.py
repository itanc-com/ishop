from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductRead, ProductUpdate


class ProductEdit:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int, product_update: ProductUpdate) -> ProductRead:
        try:
            product = await self.product_repository.update(product_id, product_update)
            if not product:
                raise EntityNotFoundException(
                    data={"product_id": product_id},
                    message="Product not found",
                )
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e), data={"product_id": product_id})

        return ProductRead.model_validate(product)
