from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends

from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult, success_response_builder

from .depends import get_user_repository
from .repository_interface import UserRepositoryInterface
from .schemas import UserCreate, UserRead
from .usecases.user_delete import UserDelete
from .usecases.user_register import UserRegister

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[],
)


@router.post(
    "/",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseSuccessDoc.HTTP_201_CREATED("User created successfully", UserRead),
        **ResponseErrorDoc.HTTP_409_CONFLICT("User already exists"),
    },
)
async def user_register(
    request: Request,
    user_schema: UserCreate,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[UserRead]:
    user_register = UserRegister(user_repository)

    user_read = await user_register.execute(user_schema)

    result = SuccessResult[UserRead](
        code=SuccessCodes.CREATED,
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
        data=user_read,
    )

    return success_response_builder(result, request)


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User deleted successfully", None),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("User not found"),
    },
)
async def user_delete(
    request: Request,
    user_id: int,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[None]:
    await UserDelete(user_repository).execute(user_id)
    result = SuccessResult[None](
        code=SuccessCodes.SUCCESS,
        message="User deleted successfully",
        status_code=status.HTTP_200_OK,
        data=None,
    )
    return result.to_json_response(request)
