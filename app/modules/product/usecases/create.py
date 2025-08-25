from app.common.exceptions.app_exceptions import DatabaseOperationException, DuplicateEntryException
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductInCreate, ProductRead

from .sku_exists import ProductSkuExists


class ProductCreate:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository
        self.sku_exists_uc = ProductSkuExists(product_repository)

    async def execute(self, product_create: ProductInCreate) -> ProductRead | None:
        # Check for duplicate SKU before insert
        if await self.sku_exists_uc.execute(product_create.sku):
            raise DuplicateEntryException("sku", product_create.sku)

        product_data = Product(**product_create.model_dump())

        try:
            product = await self.product_repository.create(product_data)
        except Exception as e:
            raise DatabaseOperationException(
                operation="insert", message=str(e), data={"product": product_create.model_dump()}
            )

        return ProductRead.model_validate(product)
