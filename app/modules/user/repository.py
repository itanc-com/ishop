from sqlalchemy import Column
from sqlalchemy.orm import Session

from app.common.exceptions.app_exceptions import UserEmailAlreadyExistsException
from app.utils.security.password_context import PasswordContext

from .models import User
from .schemas import UserInsert


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def _check_email_exits(self, email: str | Column[str]) -> bool:
        return self.session.query(User).filter(User.email == email).first() is not None

    def create(self, data: UserInsert) -> User:
        data.password = PasswordContext.hash_password(data.password)
        user = User(**data.model_dump())

        if self._check_email_exits(user.email):
            raise UserEmailAlreadyExistsException

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
