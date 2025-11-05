from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from app.common.http_response.doc_responses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.product.schemas import ProductInCreate, ProductInUpdate, ProductOutPaginated, ProductOutRead
from app.modules.product.usecases.create import ProductCreate
from app.modules.product.usecases.delete import ProductDelete
from app.modules.product.usecases.get_by_id import ProductGetById
from app.modules.product.usecases.list_paginated import ProductListPaginated
from app.modules.product.usecases.update import ProductUpdate

from .depends import get_product_repository
from .repository_interface import ProductRepositoryInterface

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Product created successfully", ProductOutRead),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def create_product(
    request: Request,
    product_create: ProductInCreate,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[ProductOutRead]:
    product_read = await ProductCreate(product_repository).execute(product_create)

    result = SuccessResult[ProductOutRead](
        code=SuccessCodes.CREATED,
        message="Product created successfully",
        status_code=status.HTTP_201_CREATED,
        data=product_read,
    )

    return result.to_json_response(request)


@router.get("/{product_id}", response_model=ProductOutRead)
async def get_product(
    request: Request,
    product_id: int,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[ProductOutRead]:
    product_read = await ProductGetById(product_repository).execute(product_id)
    result = SuccessResult[ProductOutRead](
        code=SuccessCodes.SUCCESS,
        message="Product fetched successfully",
        status_code=status.HTTP_200_OK,
        data=product_read,
    )

    return result.to_json_response(request)


@router.put("/{product_id}", response_model=ProductOutRead)
async def update_product(
    request: Request,
    product_id: int,
    product_update: ProductInUpdate,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[ProductOutRead]:
    product_read = await ProductUpdate(product_repository).execute(product_id, product_update)

    result = SuccessResult[ProductOutRead](
        code=SuccessCodes.SUCCESS,
        message="Product updated successfully",
        status_code=status.HTTP_200_OK,
        data=product_read,
    )

    return result.to_json_response(request)


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Product deleted successfully", ProductOutRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Product not found"),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def delete_product(
    request: Request,
    product_id: int,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[ProductOutRead]:
    product_read = await ProductDelete(product_repository).execute(product_id)

    result = SuccessResult[ProductOutRead](
        code=SuccessCodes.SUCCESS,
        message=f"Product with ID {product_id} deleted successfully",
        status_code=status.HTTP_200_OK,
        data=product_read,
    )

    return result.to_json_response(request)


@router.get("/", response_model=SuccessResponse[ProductOutPaginated])
async def list_all_products(
    request: Request,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
    category_id: int | None = None,
    page: int = 1,
    limit: int = 10,
) -> SuccessResponse[ProductOutPaginated]:
    product_list_paginated = await ProductListPaginated(product_repository).execute(
        category_id=category_id, page=page, limit=limit
    )

    result = SuccessResult[ProductOutPaginated](
        code=SuccessCodes.SUCCESS,
        message=f"{product_list_paginated.pagination.total_items} item(s) are listed successfully",
        status_code=status.HTTP_200_OK,
        data=product_list_paginated,
    )

    return result.to_json_response(request)
