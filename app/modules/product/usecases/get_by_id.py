from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductRead


class ProductGetById:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int) -> ProductRead:
        try:
            product: Product = await self.product_repository.get_by_id(product_id)
        except Exception as e:
            raise DatabaseOperationException(operation="select", message=str(e), data={"product_id": product_id})

        if not product:
            raise EntityNotFoundException(data={"product_id": product_id}, message="Product not found")

        return ProductRead.model_validate(product)
