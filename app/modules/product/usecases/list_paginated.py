from app.common.exceptions.app_exceptions import InternalServerException
from app.common.http_response.error_response import ErrorCodes
from app.common.schemas.pagination import PaginationInfo

from ..models import Product
from ..repository_interface import ProductRepositoryInterface
from ..schemas import ProductOutPaginated, ProductOutRead


class ProductListPaginated:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def execute(self, category_id: int | None = None, page: int = 1, limit: int = 10) -> ProductOutPaginated:
        try:
            skip = (page - 1) * limit

            # Get total count for pagination
            total_items = await self.product_repository.count_all(category_id=category_id)

            # Get products for current page
            products: list[Product] = await self.product_repository.list_all(
                category_id=category_id, skip=skip, limit=limit
            )

        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to retrieve products",
                data={"category_id": category_id, "page": page, "limit": limit},
            ) from e

        # Calculate pagination info
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        return ProductOutPaginated(
            items=[ProductOutRead.model_validate(product) for product in products],
            pagination=PaginationInfo(
                page=page,
                limit=limit,
                total_items=total_items,
                total_pages=total_pages,
                has_next=has_next,
                has_prev=has_prev,
            ),
        )
