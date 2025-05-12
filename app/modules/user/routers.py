from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.common.exceptions.app_exceptions import DuplicateEntryException
from app.common.http_response.reponses import ResponseError
from app.db.session import get_session

from .repository import UserRepository
from .schemas import UserInsert, UserView

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[],
)


@router.post(
    "/register",
    response_model=UserView,
    status_code=status.HTTP_201_CREATED,
    responses={
        **ResponseError.HTTP_409_CONFLICT("User already exists"),
    },
)
async def register_user(user_register_data: UserInsert, session: Annotated[Session, Depends(get_session)]) -> UserView:
    try:
        user = UserRepository(session).create(user_register_data)
        return user
    except DuplicateEntryException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
