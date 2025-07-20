from typing import Annotated

from fastapi import Depends, status
from fastapi.requests import Request

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_result import SuccessResult
from app.modules.category.depends import get_category_repository
from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.routers import router
from app.modules.category.schemas import CategoryRead
from app.modules.category.usecases.category_get_by_id import CategoryGetById


@router.get(
    "/{category_id}",
    response_model=CategoryRead,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Category retrieved successfully", CategoryRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("Category not found"),
    },
)
async def category_get_by_id(
    request: Request,
    category_id: int,
    category_repository: Annotated[CategoryRepositoryInterface, Depends(get_category_repository)],
) -> CategoryRead:
    category_by_id_usecase = CategoryGetById(category_repository)

    category_read = await category_by_id_usecase.execute(category_id)

    return SuccessResult[CategoryRead](
        code=status.HTTP_200_OK,
        message="Category retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=category_read,
    ).to_json_response(request)
