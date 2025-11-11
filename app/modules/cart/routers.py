from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.enums import UserRole
from app.common.http_response.doc_responses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessResponse
from app.common.http_response.success_result import SuccessCodes, SuccessResult
from app.modules.auth.depends import get_current_user_id, role_required
from app.modules.product.depends import get_product_repository
from app.modules.product.repository_interface import ProductRepositoryInterface

from .depends import get_cart_repository
from .repository_interface import CartRepositoryInterface
from .schemas import CartInCreate, CartItemInCreate, CartItemInUpdate, CartItemOutRead, CartOutRead
from .usecases import (
    AddItemToCart,
    CartCreateFromBulkItems,
    ClearCart,
    ReadCart,
    RefreshCart,
    RemoveItemFromCart,
    UpdateCartItemQuantity,
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
    responses={**ResponseErrorDoc.HTTP_401_UNAUTHORIZED("Not authenticated")},
    dependencies=[Depends(role_required([UserRole.USER, UserRole.ADMIN]))],
)


@router.post(
    "/",
    response_model=SuccessResponse[CartOutRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("All items added to cart", CartOutRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("Cart already exists"),
    },
)
async def cart_bulk_create(
    request: Request,
    cart_in_create: CartInCreate,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartOutRead]:
    cart_read = await CartCreateFromBulkItems(cartitem_repository, product_repository).execute(cart_in_create, user_id)
    result = SuccessResult[CartOutRead](
        code=SuccessCodes.CREATED,
        message="Cart created successfully",
        status_code=status.HTTP_201_CREATED,
        data=cart_read,
    )
    return result.to_json_response(request=request)


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[CartOutRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Cart retrieved", CartOutRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Cart not found"),
    },
)
async def get_cart(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartOutRead]:
    cart_read: CartOutRead = await ReadCart(cartitem_repository, product_repository).execute(user_id)

    result = SuccessResult[CartOutRead](
        code=SuccessCodes.SUCCESS,
        message="Cart retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=cart_read,
    )
    return result.to_json_response(request=request)


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Cart cleared", None),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Cart not found"),
    },
)
async def clear_cart(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
) -> SuccessResponse[None]:
    await ClearCart(cartitem_repository).execute(user_id)
    result = SuccessResult[None](
        code=SuccessCodes.SUCCESS,
        message="Cart cleared successfully",
        status_code=status.HTTP_200_OK,
        data=None,
    )
    return result.to_json_response(request=request)


@router.post(
    "/items",
    response_model=SuccessResponse[CartOutRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Item added to cart", CartOutRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("Item already in cart"),
    },
)
async def add_item(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cart_item_create: CartItemInCreate,
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartItemOutRead]:
    item_read = await AddItemToCart(cartitem_repository, product_repository).execute(cart_item_create, user_id=user_id)

    result = SuccessResult[CartItemOutRead](
        code=SuccessCodes.CREATED,
        message="Item added to cart successfully",
        status_code=status.HTTP_201_CREATED,
        data=item_read,
    )
    return result.to_json_response(request=request)


@router.patch(
    "/{user_id}/items/{product_id}",
    response_model=SuccessResponse[CartItemOutRead],
    status_code=status.HTTP_200_OK,
    summary="Update item quantity in cart",
    description="""
    Update the quantity of a specific item in the user's cart.

    **Behavior:**
    - Sets the cart item to the **exact quantity** specified (not incremental)
    - If quantity = 0, the item is removed from the cart (returns None)
    - If quantity > 0, updates to that exact quantity and recalculates subtotal
    - Returns full cart item details including product title, SKU, and price

    **Example Use Cases:**
    - User changes quantity dropdown from 3 to 5 → send quantity: 5
    - User manually types 10 in quantity input → send quantity: 10
    - User sets quantity to 0 to remove item → send quantity: 0

    **Important:**
    - Quantity must be > 0
    - This endpoint uses **absolute quantity**, not delta/increment
    - Product details (title, SKU) are fetched fresh to ensure accuracy
    """,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Item quantity updated", CartItemOutRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Item not found in cart"),
        **ResponseErrorDoc.HTTP_400_BAD_REQUEST("Invalid quantity (must be > 0)"),
    },
)
async def update_item_quantity(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cart_item_update: CartItemInUpdate,
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartItemOutRead | None]:
    updated_item = await UpdateCartItemQuantity(cartitem_repository, product_repository).execute(
        user_id, cart_item_update
    )

    result = SuccessResult[CartItemOutRead | None](
        code=SuccessCodes.SUCCESS,
        message="Item quantity updated" if cart_item_update.quantity > 0 else "Item removed from cart",
        status_code=status.HTTP_200_OK,
        data=updated_item,
    )
    return result.to_json_response(request=request)


@router.delete(
    "/{user_id}/items/{product_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Item removed from cart", CartItemOutRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Item not found in cart"),
    },
)
async def remove_item(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    product_id: int,
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
) -> SuccessResponse[None]:
    await RemoveItemFromCart(cartitem_repository).execute(user_id, product_id)
    result = SuccessResult[None](
        code=SuccessCodes.SUCCESS,
        message="Item removed from cart successfully",
        status_code=status.HTTP_200_OK,
        data=None,
    )
    return result.to_json_response(request=request)


@router.post(
    "/{user_id}/refresh",
    response_model=SuccessResponse[CartOutRead],
    status_code=status.HTTP_200_OK,
    summary="Refresh cart with latest product prices and details",
    description="""
    Updates all cart items to reflect the latest product price, title, and SKU.
    Returns the updated cart.
    """,
)
async def refresh_cart(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    cartitem_repository: Annotated[CartRepositoryInterface, Depends(get_cart_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartOutRead]:
    refreshed_cart = await RefreshCart(cartitem_repository, product_repository).execute(user_id)

    result = SuccessResult[CartOutRead](
        code=SuccessCodes.SUCCESS,
        message="Cart refreshed with latest product details",
        status_code=status.HTTP_200_OK,
        data=refreshed_cart,
    )

    return result.to_json_response(request=request)
