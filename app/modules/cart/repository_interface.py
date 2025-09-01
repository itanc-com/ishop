from abc import ABC, abstractmethod

from .dtos import CartItemWithProductDTO
from .models import CartItem


class CartItemRepositoryInterface(ABC):
    model_class = CartItem

    @abstractmethod
    async def bulk_insert(self, cart_items: list[CartItem]) -> list[CartItem]:
        """
        Insert multiple cart items in a single database operation.

        Args:
            cart_items: List of CartItem objects to insert

        Returns:
            List of inserted CartItem objects with populated IDs and timestamps
        """
        pass

    @abstractmethod
    async def insert(self, cart_item: CartItem) -> CartItem:
        """
        Insert a single cart item into the database.

        Args:
            cart_item: CartItem object to insert

        Returns:
            The inserted CartItem object with populated ID and timestamps
        """
        pass

    @abstractmethod
    async def remove(self, user_id: int, product_id: int) -> None:
        """
        Remove a specific cart item for a user and product.

        Args:
            user_id: The user ID
            product_id: The product ID
        """
        pass

    @abstractmethod
    async def find_all(self, user_id: int) -> list[CartItem]:
        """
        Retrieve all cart items for a specific user.

        Args:
            user_id: The user ID to fetch cart items for

        Returns:
            List of CartItem objects for the user (empty list if no items)
        """
        pass

    @abstractmethod
    async def find_all_with_products(self, user_id: int) -> list[CartItemWithProductDTO]:
        """
        Retrieve all cart items for a specific user with product details.

        Args:
            user_id: The user ID to fetch cart items for

        Returns:
            List of CartItemWithProductDTO containing cart item and product data
        """
        pass

    @abstractmethod
    async def get_item(self, user_id: int, product_id: int) -> CartItem | None:
        """
        Retrieve a specific cart item for a user and product combination.

        Args:
            user_id: The user ID
            product_id: The product ID

        Returns:
            CartItem object if found, None if not found
        """
        pass

    @abstractmethod
    async def clear_cart(self, user_id: int) -> None:
        """
        Remove all cart items for a specific user.

        Args:
            user_id: The user ID whose cart should be cleared
        """
        pass

    @abstractmethod
    async def has_cart_items(self, user_id: int) -> bool:
        """
        Check if user has any items in their cart.

        Args:
            user_id: The user ID to check

        Returns:
            True if user has any items in cart, False if cart is empty
        """
        pass
