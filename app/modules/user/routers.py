from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends

from app.common.http_response.doc_responses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult
from app.modules.user.usecases.user_get_by_id import UserGetById

from .depends import get_user_repository
from .repository_interface import UserRepositoryInterface
from .schemas import UserCreate, UserRead
from .usecases.user_delete_by_email import UserDeleteByEmail
from .usecases.user_delete_by_id import UserDeleteById
from .usecases.user_get_by_email import UserGetByEmail
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

    return result.to_json_response(request)


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User retrieved successfully", UserRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("User not found"),
    },
)
async def get_user_by_id(
    request: Request,
    user_id: int,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[UserRead]:
    get_user_by_id = UserGetById(user_repository)
    user_read = await get_user_by_id.execute(user_id)

    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User retrieved successfully",
        status_code=status.HTTP_200_OK,
        data=user_read,
    )
    return result.to_json_response(request)


@router.get(
    "/by_email/{user_email}",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User fetched successfully", UserRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("User not found"),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def get_user_by_email(
    request: Request,
    user_email: str,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[UserRead]:
    get_user_by_email = UserGetByEmail(user_repository)
    user_read = await get_user_by_email.execute(user_email)

    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message="User fetched successfully",
        status_code=status.HTTP_200_OK,
        data=user_read,
    )
    return result.to_json_response(request)


@router.delete(
    "/{user_id}",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User deleted successfully", UserRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("User not found"),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def user_delete(
    request: Request,
    user_id: int,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[UserRead]:
    user_read = await UserDeleteById(user_repository).execute(user_id)

    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message=f"User with id {user_id} deleted successfully",
        status_code=status.HTTP_200_OK,
        data=UserRead.model_validate(user_read),
    )

    return result.to_json_response(request)


@router.delete(
    "/by_email/{user_email}",
    response_model=SuccessResponse[UserRead],
    status_code=status.HTTP_200_OK,
    responses={
        **ResponseSuccessDoc.HTTP_200_OK("User deleted successfully", UserRead),
        **ResponseErrorDoc.HTTP_404_NOT_FOUND("User not found"),
        **ResponseErrorDoc.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    },
)
async def user_delete_by_email(
    request: Request,
    user_email: str,
    user_repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
) -> SuccessResponse[UserRead]:
    user_read = await UserDeleteByEmail(user_repository).execute(user_email)

    result = SuccessResult[UserRead](
        code=SuccessCodes.SUCCESS,
        message=f"User with email {user_email} deleted successfully",
        status_code=status.HTTP_200_OK,
        data=UserRead.model_validate(user_read),
    )

    return result.to_json_response(request)
