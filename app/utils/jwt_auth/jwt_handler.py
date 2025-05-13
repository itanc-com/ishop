from jose import ExpiredSignatureError, jwt, JWTError
from app.common.exceptions import CredentialsException
from typing import Any
from app.utils.jwt_auth.auth_config import JWT_SECRET_KEY, JWT_ISSUER_SERVER, JWT_ALGORITHM


class JWThandler:
    
    @staticmethod
    def create_token(payload: dict[str, Any]) -> str:
        return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    @staticmethod
    def read_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM, issuer=JWT_ISSUER_SERVER, options={"verify_exp": True})
        except ExpiredSignatureError:
            raise CredentialsException("EXPIRED TOKEN")
        except JWTError:
            raise CredentialsException("UNVERIFIED SIGNATURE")

   