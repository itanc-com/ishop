from abc import ABC, abstractmethod

from .dtos import CartItemDTO
from .models import CartItem


class CartRepositoryInterface(ABC):
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
    async def update(self, cart_item: CartItem) -> CartItem:
        """
        Update a single cart item in the database.

        Args:
            cart_item: CartItem object to update

        Returns:
            The updated CartItem object
        """
        pass

    @abstractmethod
    async def delete(self, user_id: int, product_id: int) -> None:
        """
        Remove a specific cart item for a user and product.

        Args:
            user_id: The user ID
            product_id: The product ID
        """
        pass

    @abstractmethod
    async def bulk_update(self, cart_items: list[CartItem]) -> None:
        """
        Update multiple cart items in a single database operation.

        Args:
            cart_items: List of CartItem SQLAlchemy models to update

        Note:
            - user_id and product_id are primary keys and won't be updated
            - Updates: quantity, price, subtotal, date_modified
        """
        pass

    @abstractmethod
    async def bulk_delete(self, user_id: int, product_ids: list[int]) -> None:
        """
        Delete multiple cart items for a user in a single database operation.

        Args:
            user_id (int): The ID of the user whose cart items will be deleted.
            product_ids (list[int]): List of product IDs to delete from the user's cart.

        Notes:
            - Efficiently removes all specified items in one query.
            - If product_ids is empty, no items will be deleted.
            - Use for batch removal of items (e.g., cart sync, clear, or update).
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
    async def find_all_with_products(self, user_id: int) -> list[CartItemDTO]:
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
    async def has_item(self, user_id: int, product_id: int) -> bool:
        """
        Check if a specific item exists in user's cart.

        Args:
            user_id: The user ID
            product_id: The product ID

        Returns:
            True if the item exists in cart, False otherwise
        """
        pass

    @abstractmethod
    async def delete_all_items(self, user_id: int) -> None:
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
