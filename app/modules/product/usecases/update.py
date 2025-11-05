from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductInUpdate, ProductOutRead


class ProductUpdate:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int, product_update: ProductInUpdate) -> ProductOutRead:
        try:
            product = await self.product_repository.update_by_id(product_id, product_update)
            if not product:
                raise EntityNotFoundException(
                    data={"product_id": product_id},
                    message="Product not found",
                )
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e), data={"product_id": product_id})

        return ProductOutRead.model_validate(product)
