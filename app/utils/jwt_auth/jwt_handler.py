from datetime import datetime, timezone
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
            return jwt.decode(
                token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM, issuer=JWT_ISSUER_SERVER, options={"verify_exp": True}
            )
        except JWTError as e:
            raise ValueError(e) from e

    @staticmethod
    def verify_token(token_payload: dict[str, Any], expected_payload: dict[str, Any]) -> bool:
        try:
            current_time = datetime.now(timezone.utc).replace(microsecond=0)
            expiration_time = token_payload.get("exp", 0)

            if expiration_time < int(current_time.timestamp()):
                return False

            keys_to_check = {"typ", "role", "iss"}

            for key in keys_to_check:
                if key in expected_payload and token_payload.get(key) not in expected_payload[key]:
                    return False

            return True

        except JWTError as e:
            raise ValueError(e) from e
