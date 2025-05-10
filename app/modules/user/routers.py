from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.common.exceptions.app_exceptions import UserEmailAlreadyExistsException
from app.db.session import get_session
from app.modules.user.repository import UserRepository

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
)
async def register_user(user_register_data: UserInsert, session: Annotated[Session, Depends(get_session)]) -> UserView:
    try:
        user = UserRepository(session).create(user_register_data)
        return user
    except UserEmailAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "message": str(e),
                "type": "user_email_exists",
            },
        )
