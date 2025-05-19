from typing import Annotated

from fastapi import APIRouter, Request, status
from fastapi.params import Depends

from app.common.fastapi.depends import get_user_repository
from app.common.http_response.doc_reponses import ResponseErrorDoc, ResponseSuccessDoc
from app.common.http_response.success_response import SuccessCodes, SuccessResponse
from app.common.http_response.success_result import SuccessResult, success_response_builder

from .repository_interface import UserRepositoryInterface
from .schemas import UserCreate, UserRead
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

