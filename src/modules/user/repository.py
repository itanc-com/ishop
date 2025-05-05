from sqlalchemy.orm import Session


class UserRepository:
    def __init__(self, session: Session):
        self.session = session
