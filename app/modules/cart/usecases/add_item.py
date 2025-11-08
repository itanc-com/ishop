from app.common.exceptions.app_exceptions import (
    DatabaseOperationException,
    DuplicateEntryException,
    EntityNotFoundException,
)
from app.modules.cart.repository_interface import CartItemRepositoryInterface
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartItemInCreate, CartItemOutRead


class AddItemToCart:
    def __init__(
        self,
        cart_item_repository: CartItemRepositoryInterface,
        product_repository: ProductRepositoryInterface,
    ) -> None:
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def execute(self, cart_item_create: CartItemInCreate) -> CartItemOutRead | None:
        product: Product | None = await self.product_repository.get_by_id(cart_item_create.product_id)

        if not product:
            raise EntityNotFoundException(
                data={"product_id": cart_item_create.product_id},
                message=f"Product with id {cart_item_create.product_id} not found",
            )

        # Extract product attributes while session is still active
        product_title = product.title
        product_sku = product.sku
        product_price = float(product.price)

        try:
            item_already_in_cart = await self.cart_item_repository.has_item(
                user_id=cart_item_create.user_id,
                product_id=cart_item_create.product_id,
            )

        except Exception as e:
            raise DatabaseOperationException(
                operation="select",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        #! it should increase the quantity of the card
        # * need to call another usecase to increase the quantity of this product in cart
        if item_already_in_cart:
            raise DuplicateEntryException(field="product_id", value=str(cart_item_create.product_id))

        # Create cart item with calculated price and total
        cart_item_data = CartItem(
            **cart_item_create.model_dump(),  # Gets user_id, product_id, quantity
            price=float(product_price),  # Add calculated price from extracted product price
            total=float(product_price) * cart_item_create.quantity,  # Add calculated total
        )

        try:
            # Repository now returns a fresh instance with all auto-generated fields
            cart_item = await self.cart_item_repository.insert(cart_item_data)

        except Exception as e:
            raise DatabaseOperationException(
                operation="insert",
                message=str(e),
                data={"user_id": cart_item_create.user_id, "product_id": cart_item_create.product_id},
            )

        new_cart_item = CartItemOutRead(
            user_id=cart_item.user_id,
            product_id=cart_item.product_id,
            quantity=cart_item.quantity,
            title=product_title,  # Use extracted title instead of product.title
            sku=product_sku,  # Use extracted sku instead of product.sku
            price=cart_item.price,
            total=cart_item.total,
            date_created_gmt=cart_item.date_created,
            date_modified_gmt=cart_item.date_modified,
        )

        return new_cart_item
