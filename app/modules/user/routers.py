from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.common.http_response.reponses import ResponseError, ResponseSuccess
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult, success_response
from app.db.session import get_session

from .repository import UserRepository
from .schemas import UserCreate, UserRead

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
        **ResponseSuccess.HTTP_201_CREATED("User created successfully", UserRead),
        **ResponseError.HTTP_409_CONFLICT("User already exists"),
    },
)
async def user_register(
    request: Request, user_register_data: UserCreate, session: Annotated[Session, Depends(get_session)]
) -> SuccessResponse[UserRead]:
    user = UserRepository(session).create(user_register_data)
    result = SuccessResult[UserRead](
        code=SuccessCodes.CREATED,
        message="User created successfully",
        status_code=status.HTTP_201_CREATED,
        data=UserRead.model_validate(user),
    )
    return success_response(result, request)
