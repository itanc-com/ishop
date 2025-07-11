from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.category.depends import get_category_repository
from app.modules.category.repository_interface import CategoryRepositoryInterface
from app.modules.category.schemas import CategoryCreate, CategoryRead
from app.modules.category.usecases.category_create import CreateCategory

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[],
)


@router.post(
    "/",
    response_model=SuccessResponse[CategoryRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("Category created successfully", CategoryRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("Category already exists"),
    },
)
async def category_create(
    request: Request,
    category_schema: CategoryCreate,
    category_repository: Annotated[CategoryRepositoryInterface, Depends(get_category_repository)],
) -> JSONResponse:
    create_category_usecase = CreateCategory(category_repository)

    category_read = await create_category_usecase.execute(category_schema)

    result = SuccessResult[CategoryRead](
        code=SuccessCodes.CREATED,
        message="Category created successfully",
        status_code=status.HTTP_201_CREATED,
        data=category_read,
    )

    return result.to_json_response(request)
