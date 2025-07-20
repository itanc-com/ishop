from typing import Annotated

from fastapi import Depends, Request, status
from fastapi.params import Query
from fastapi.responses import JSONResponse

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.category.depends import get_category_repository
from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.routers import router
from app.modules.category.schemas import CategoryRead
from app.modules.category.usecases.category_list import CategoryList


@router.get(
    "/",
    response_model=SuccessResponse[list[CategoryRead]],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("Categories fetched successfully", list[CategoryRead]),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def category_list(
    request: Request,
    category_repository: Annotated[CategoryRepositoryInterface, Depends(get_category_repository)],
    parent_id: int = Query(0, description="Parent category ID", examples=[1], ge=0),
) -> JSONResponse:
    category_list_usecase = CategoryList(category_repository)
    categories = await category_list_usecase.execute(parent_id)

    return SuccessResult[list[CategoryRead]](
        code=SuccessCodes.SUCCESS,
        message="Categories fetched successfully",
        status_code=status.HTTP_200_OK,
        data=categories,
    ).to_json_response(request)
