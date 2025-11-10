from app.common.exceptions.app_exceptions import InternalServerException, NotFoundException
from app.common.http_response.error_response import ErrorCodes
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductOutRead


class ProductGetById:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, product_id: int) -> ProductOutRead:
        try:
            product: Product | None = await self.product_repository.get_by_id(product_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve product", data={"product_id": product_id}
            ) from e

        if not product:
            raise NotFoundException(data={"product_id": product_id}, message="Product not found")

        return ProductOutRead.model_validate(product)
