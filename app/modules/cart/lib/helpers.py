def merge_cart_items(items: list[dict[str, int]]) -> list[dict[str, int]]:
    """
    Merge duplicate product items by summing their quantities.

    Args:
        items: List of cart items with product_id and quantity keys.

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
        product_id = item["product_id"]
        quantity = item["quantity"]
        merged[product_id] = merged.get(product_id, 0) + quantity

    return [{"product_id": pid, "quantity": qty} for pid, qty in merged.items()]
