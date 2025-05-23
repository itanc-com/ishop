from app.common.exceptions.app_exceptions import DatabaseOperationException, EntityNotFoundException
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductRead


class ProductListAll:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, category_id: int | None = None, page: int = 1, per_page: int = 10) -> list[ProductRead]:
        try:
            skip = (page - 1) * per_page
            products: list[Product] = await self.product_repository.list_all(
                category_id=category_id, skip=skip, limit=per_page
            )
            if not products:
                raise EntityNotFoundException(
                    data={"category_id": category_id, "page": page, "per_page": per_page}, message="No products found"
                )
        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
                data={"category_id": category_id, "page": page, "per_page": per_page},
            )

        return [ProductRead.model_validate(product) for product in products]
