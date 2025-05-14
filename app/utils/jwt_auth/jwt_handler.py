from typing import Any

from jose import JOSEError, JWTError, jwt

from app.utils.jwt_auth.auth_config import JWT_ALGORITHM, JWT_ISSUER_SERVER, JWT_SECRET_KEY


class JWThandler:
    
    @staticmethod
    def create_token(payload: dict[str, Any]) -> str:
        try:
            return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        except JOSEError as e:
            raise ValueError(e) from e

    @staticmethod
    def read_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM, issuer=JWT_ISSUER_SERVER, options={"verify_exp": True})
        except JWTError as e:
            raise ValueError(e) from e


   