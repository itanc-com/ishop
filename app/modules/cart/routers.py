from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult

from .depends import get_cartitem_repository
from .repository_interface import CartItemRepositoryInterface
from .schemas import CartBulkCreate, CartRead
from .usecases import CreateCartFromItems

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
    dependencies=[],
)


@router.post(
    "/",
    response_model=SuccessResponse[CartRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("All items added to cart", CartRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("Cart already exists"),
    },
)
async def cart_bulk_create(
    request: Request,
    cart_schema: CartBulkCreate,
    cartitem_repository: Annotated[CartItemRepositoryInterface, Depends(get_cartitem_repository)],
) -> SuccessResponse[CartRead]:
    cart_read: CartRead | None = await CreateCartFromItems(cartitem_repository).execute(cart_schema)

    result = SuccessResult[cart_read](
        code=SuccessCodes.CREATED,
        message="Cart created successfully",
        status_code=status.HTTP_201_CREATED,
        data=cart_schema,
    )

    return result.to_json_response(request=request)
