from app.common.exceptions.app_exceptions import ConflictException, InternalServerException
from app.common.http_response.error_response import ErrorCodes
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductInCreate, ProductOutRead

from .sku_exists import ProductSkuExists


class ProductCreate:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository
        self.sku_exists_uc = ProductSkuExists(product_repository)

    async def execute(self, product_create: ProductInCreate) -> ProductOutRead | None:
        # Check for duplicate SKU before insert
        if await self.sku_exists_uc.execute(product_create.sku):
            raise ConflictException(
                code=ErrorCodes.DUPLICATE_ENTRY,
                message="Product with the same SKU already exists",
                data={"sku": product_create.sku},
            )

        product_data = Product(**product_create.model_dump())

        try:
            product: Product = await self.product_repository.create(product_data)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR,
                message="Failed to insert new product",
                data={"product": product_create.model_dump()},
            ) from e

        return ProductOutRead.model_validate(product)
