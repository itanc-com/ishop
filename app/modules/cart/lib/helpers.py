from typing import Any


def merge_cart_items(items: list[dict[str, int] | Any]) -> list[dict[str, int]]:
    """
    Merge duplicate product items by summing their quantities.

    Args:
        items: List of cart items (dicts or Pydantic models) with product_id and quantity.

    Returns:
        List of merged cart items with unique product_ids and summed quantities.

    Example:
        >>> items = [
        ...     {"product_id": 3, "quantity": 2},
        ...     {"product_id": 9, "quantity": 1},
        ...     {"product_id": 9, "quantity": 5}
        ... ]
        >>> merge_cart_items(items)
        [{'product_id': 3, 'quantity': 2}, {'product_id': 9, 'quantity': 6}]
    """
    merged: dict[int, int] = {}

    # accumulate quantities for each product_id
    for item in items:
        # Handle both dict and Pydantic models
        product_id = item["product_id"] if isinstance(item, dict) else item.product_id
        quantity = item["quantity"] if isinstance(item, dict) else item.quantity
        merged[product_id] = merged.get(product_id, 0) + quantity

    return [{"product_id": pid, "quantity": qty} for pid, qty in merged.items()]
