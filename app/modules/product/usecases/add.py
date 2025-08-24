from app.common.exceptions.app_exceptions import DatabaseOperationException, DuplicateEntryException
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface
from app.modules.product.schemas import ProductCreate, ProductRead


class ProductAdd:
    def __init__(self, product_repository: ProductRepositoryInterface) -> None:
        self.product_repository = product_repository

    async def is_sku_exist(self, sku: str) -> bool:
        return await self.product_repository.exists_by_field("sku", sku)

    async def execute(self, product_create: ProductCreate) -> ProductRead | None:
        # Check for duplicate SKU before insert
        if await self.is_sku_exist(product_create.sku):
            raise DuplicateEntryException("sku", product_create.sku)

        product_data = Product(**product_create.model_dump())

        try:
            product = await self.product_repository.create(product_data)
        except Exception as e:
            raise DatabaseOperationException(
                operation="insert", message=str(e), data={"product": product_create.model_dump()}
            )

        return ProductRead.model_validate(product)
