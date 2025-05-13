from sqlalchemy.orm import Session

from app.common.exceptions.app_exceptions import DuplicateEntryException
from app.utils.security.password_context import PasswordContext

from .models import User
from .schemas import UserCreate


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserCreate) -> User:
        data.password = PasswordContext.hash_password(data.password)

        if self.get_by_email(data.email) is not None:
            raise DuplicateEntryException("email", data.email)

        user = User(**data.model_dump())
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()
