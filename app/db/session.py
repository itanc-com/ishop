from typing import Generator

from sqlalchemy.orm import Session

from .base import SessionLocal


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
