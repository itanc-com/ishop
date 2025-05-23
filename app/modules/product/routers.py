from typing import Annotated

import orjson
from fastapi import APIRouter, Request, Response, status
from fastapi.params import Depends

from app.common.fastapi.depends import get_product_repository
from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.product.usecases.add import ProductAdd
from app.modules.product.usecases.delete import ProductDelete
from app.modules.product.usecases.edit import ProductEdit
from app.modules.product.usecases.get_by_id import ProductGetById
from app.modules.product.usecases.list_all import ProductListAll

from .repository_interface import ProductRepositoryInterface
from .schemas import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Product created successfully", ProductRead),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def create_product(
    request: Request,
    product_create: ProductCreate,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> SuccessResponse[ProductRead]:
    product_read = await ProductAdd(product_repository).execute(product_create)

    result = SuccessResult[ProductRead](
        code=SuccessCodes.CREATED,
        message="Product created successfully",
        status_code=status.HTTP_201_CREATED,
        data=product_read,
    )
    return result.to_json_response(request)


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(
    product_id: int, product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)]
) -> ProductRead:
    product_read = await ProductGetById(product_repository).execute(product_id)
    return product_read


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
) -> ProductRead:
    product_read = await ProductEdit(product_repository).execute(product_id, product_update)
    return product_read


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Product not found"),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def delete_product(
    product_id: int,
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
    response: Response,
):
    product_read = await ProductDelete(product_repository).execute(product_id)
    response.headers["X-Deleted-Product"] = orjson.dumps(product_read.model_dump()).decode()
    return None


@router.get("/", response_model=list[ProductRead])
async def list_all_products(
    product_repository: Annotated[ProductRepositoryInterface, Depends(get_product_repository)],
    category_id: int | None = None,
    page: int = 1,
    per_page: int = 10,
) -> list[ProductRead]:
    products = await ProductListAll(product_repository).execute(category_id=category_id, page=page, per_page=per_page)
    return products
