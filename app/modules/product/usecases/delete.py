from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductRead


class ProductDelete:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int) -> ProductRead:
        product = None

        try:
            product = await self.product_repository.delete(product_id)
        except Exception as e:
            raise DatabaseOperationException(operation="delete", message=str(e), data={"product_id": product_id})

        if not product:
            raise EntityNotFoundException(
                data={"product_id": product_id}, message=f"Product with ID {product_id} not found."
            )

        return ProductRead.model_validate(product)
