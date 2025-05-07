from passlib.context import CryptContext

class PasswordContext:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return PasswordContext.pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        return PasswordContext.pwd_context.hash(plain_password)

    @staticmethod
    def needs_rehash_password(hashed_password: str) -> bool:
        return PasswordContext.pwd_context.needs_update(hashed_password)

    @staticmethod
    def verify_and_update(plain_password: str, hashed_password: str) -> tuple | None:
        return PasswordContext.pwd_context.verify_and_update(
            plain_password, hashed_password
        )