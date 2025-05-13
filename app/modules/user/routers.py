from typing import Annotated

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.common.http_response.reponses import ResponseError
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
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseError.HTTP_409_CONFLICT("User already exists"),
    },
)
async def register_user(user_register_data: UserCreate, session: Annotated[Session, Depends(get_session)]) -> UserRead:
        user = UserRepository(session).create(user_register_data)
        return user
   
