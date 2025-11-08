from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.enums import UserRole
from app.common.http_response.doc_responses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessResponse
from app.common.http_response.success_result import SuccessCodes, SuccessResult
from app.modules.auth.depends import role_required
from app.modules.product.depends import get_product_repository
from app.modules.product.repository_interface import ProductRepositoryInterface

from .depends import get_cartitem_repository
from .repository_interface import CartItemRepositoryInterface
from .schemas import CartInCreate, CartItemInCreate, CartItemOutRead, CartOutRead
from .usecases import AddItemToCart, CartCreateFromBulkItems, ReadCart, RemoveItemFromCart

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
    dependencies=[],
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
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartOutRead]:
    cart_read = await CartCreateFromBulkItems(cartitem_repository, product_repository).execute(cart_in_create)
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
    dependencies=[Depends(role_required([UserRole.USER, UserRole.ADMIN]))],
)
async def get_cart(
    request: Request,
    user_id: int,
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
) -> SuccessResponse[CartOutRead]:
    cart_read = await ReadCart(cartitem_repository).execute(user_id)
    if not cart_read:
        result = SuccessResult[None](
            code=SuccessCodes.NOT_FOUND,
            message="Cart not found",
            status_code=status.HTTP_404_NOT_FOUND,
            data=None,
        )
        return result.to_json_response(request=request)

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
        **ResponseSuccessDoc.HTTP_200_OK("Cart cleared", CartOutRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Cart not found"),
    },
)
async def clear_cart(
    request: Request,
    user_id: int,
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
) -> SuccessResponse[None]:
    await cartitem_repository.clear_cart(user_id)
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
    cart_item_create: CartItemInCreate,
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[CartItemOutRead]:
    item_read = await AddItemToCart(cartitem_repository, product_repository).execute(cart_item_create)
    result = SuccessResult[CartItemOutRead](
        code=SuccessCodes.CREATED,
        message="Item added to cart successfully",
        status_code=status.HTTP_201_CREATED,
        data=item_read,
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
    user_id: int,
    product_id: int,
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
) -> SuccessResponse[None]:
    await RemoveItemFromCart(cartitem_repository).execute(user_id, product_id)
    result = SuccessResult[None](
        code=SuccessCodes.SUCCESS,
        message="Item removed from cart successfully",
        status_code=status.HTTP_200_OK,
        data=None,
    )
    return result.to_json_response(request=request)
