from app.common.exceptions.app_exceptions import InternalServerException
from app.common.http_response.error_response import ErrorCodes
from app.modules.cart.repository_interface import CartRepositoryInterface
from app.modules.product.models import Product
from app.modules.product.repository_interface import ProductRepositoryInterface

from ..models import CartItem
from ..schemas import CartItemOutRead, CartOutRead


class ReadCart:
    def __init__(
        self, cart_repository: CartRepositoryInterface, product_repository: ProductRepositoryInterface
    ) -> None:
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def execute(self, user_id: int) -> CartOutRead:
        """
        Retrieves and synchronizes the user's cart items with the latest product data.

        This usecase performs the following steps:
        1. Fetches all cart items for the given user.
        2. Extracts product IDs from the cart items.
        3. Fetches product details for those IDs in a single query.
        4. Builds a hash map for fast product lookup.
        5. For each cart item:
            - If the product exists, updates the cart item with the latest product title, SKU, price, and availability.
            - If the product has been removed, marks the cart item as unavailable and uses placeholder values.
        6. Returns a CartOutRead object containing the updated cart items and the total price.

        Business rules:
        - Cart items for deleted/unavailable products are kept in the cart but marked as unavailable.
        - Product price and details are always synced with the latest product data.
        - The subtotal for each item is recalculated using the current product price.

        Args:
            user_id (int): The ID of the user whose cart is being read.

        Returns:
            CartOutRead: The cart response containing all items and the total price.

        Raises:
            InternalServerException: If there is a database error.
        """

        try:
            cart_items_list_db: list[CartItem] = await self.cart_repository.find_all(user_id)
        except Exception as e:
            raise InternalServerException(
                code=ErrorCodes.DATABASE_ERROR, message="Failed to retrieve cart items", data={"user_id": user_id}
            ) from e

        if not cart_items_list_db:
            return CartOutRead(items=[], total=0.0)

        # Extract product IDs from cart items
        product_ids: list[int] = [item.product_id for item in cart_items_list_db]

        if product_ids:
            try:
                products = await self.product_repository.list_by_ids(product_ids)
                product_map = {product.id: product for product in products}
            except Exception as e:
                raise InternalServerException(
                    code=ErrorCodes.DATABASE_ERROR,
                    message="Failed to retrieve product details",
                    data={"product_ids": product_ids},
                ) from e
        else:
            product_map = {}

        CartItemsOut = []

        # Build the response cart items list
        for cart_item in cart_items_list_db:
            if cart_item.product_id not in product_map:
                CartItemsOut.append(
                    CartItemOutRead(
                        product_id=cart_item.product_id,
                        quantity=cart_item.quantity,
                        title="Product Removed",
                        sku="N/A",
                        price=cart_item.price,
                        subtotal=cart_item.subtotal,
                        is_available=False,
                        date_created_gmt=cart_item.date_created,
                        date_modified_gmt=cart_item.date_modified,
                    )
                )

            else:
                product_details: Product = product_map[cart_item.product_id]

                CartItemsOut.append(
                    CartItemOutRead(
                        product_id=product_details.id,
                        quantity=cart_item.quantity,
                        title=product_details.title,
                        sku=product_details.sku,
                        price=product_details.price,
                        subtotal=float(product_details.price) * cart_item.quantity,
                        is_available=product_details.is_available,
                        date_created_gmt=cart_item.date_created,
                        date_modified_gmt=cart_item.date_modified,
                    )
                )

        return CartOutRead(items=CartItemsOut, total=sum(item.subtotal for item in CartItemsOut))
