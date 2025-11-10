from app.modules.cart.lib.helpers import merge_cart_items


def test_merge_cart_items_empty_list():
    """Test merging an empty list returns empty list."""
    assert merge_cart_items([]) == []


def test_merge_cart_items_single_item():
    """Test merging a single item returns it unchanged."""
    items = [{"product_id": 1, "quantity": 5}]
    result = merge_cart_items(items)
    assert result == [{"product_id": 1, "quantity": 5}]


def test_merge_cart_items_no_duplicates():
    """Test merging items with unique product IDs."""
    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 5},
        {"product_id": 3, "quantity": 1},
    ]
    result = merge_cart_items(items)
    assert len(result) == 3
    assert {"product_id": 1, "quantity": 2} in result
    assert {"product_id": 2, "quantity": 5} in result
    assert {"product_id": 3, "quantity": 1} in result


def test_merge_cart_items_with_duplicates():
    """Test merging duplicate product IDs sums quantities."""
    items = [
        {"product_id": 9, "quantity": 1},
        {"product_id": 9, "quantity": 5},
    ]
    result = merge_cart_items(items)
    assert len(result) == 1
    assert result[0] == {"product_id": 9, "quantity": 6}


def test_merge_cart_items_multiple_duplicates():
    """Test merging with multiple sets of duplicates."""
    items = [
        {"product_id": 3, "quantity": 2},
        {"product_id": 9, "quantity": 1},
        {"product_id": 3, "quantity": 3},
        {"product_id": 9, "quantity": 5},
        {"product_id": 3, "quantity": 1},
    ]
    result = merge_cart_items(items)
    assert len(result) == 2
    assert {"product_id": 3, "quantity": 6} in result  # 2 + 3 + 1
    assert {"product_id": 9, "quantity": 6} in result  # 1 + 5


def test_merge_cart_items_mixed_duplicates_and_unique():
    """Test merging with both duplicates and unique items."""
    items = [
        {"product_id": 1, "quantity": 2},
        {"product_id": 2, "quantity": 5},
        {"product_id": 1, "quantity": 3},
        {"product_id": 3, "quantity": 1},
    ]
    result = merge_cart_items(items)
    assert len(result) == 3
    assert {"product_id": 1, "quantity": 5} in result  # 2 + 3
    assert {"product_id": 2, "quantity": 5} in result
    assert {"product_id": 3, "quantity": 1} in result


def test_merge_cart_items_large_quantities():
    """Test merging items with large quantity values."""
    items = [
        {"product_id": 1, "quantity": 1000},
        {"product_id": 1, "quantity": 2500},
    ]
    result = merge_cart_items(items)
    assert result == [{"product_id": 1, "quantity": 3500}]
