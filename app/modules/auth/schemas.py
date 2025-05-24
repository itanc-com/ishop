import time
from enum import Enum

from pydantic import BaseModel


class TokenType(str, Enum):
    access = "access"
    refresh = "refresh"


class JWTPayload(BaseModel):
    """
    Represents the payload section of a JSON Web Token (JWT) used for authentication
    and authorization within the application.

    Attributes:
        iss (str | None): The issuer of the token (e.g., "auth-service"). Optional.
        typ (TokenType): The type of the token, typically "access" or "refresh".
        sub (str): The subject of the token, usually the user ID as a string.
        iat (int): Issued At – The Unix timestamp indicating when the token was created.
        exp (int): Expiration – The Unix timestamp indicating when the token will expire.
        role (str): The role of the token subject (e.g., "user", "admin"). Defaults to "user".

    Notes:
        - `sub` should be set to a stable identifier like the user ID (as string).
        - `iat` and `exp` are Unix timestamps in seconds.
        - `typ` is recommended to distinguish between access and refresh tokens.
        - Do not include sensitive information like email or full name in the token payload.
    """

    iss: str | None = None
    typ: str
    sub: str
    iat: int = 0
    exp: int = 0
    role: str = "user"

    @classmethod
    def create(
        cls,
        sub: int | str,
        role: str = "user",
        expire_in: int = 3600,
        token_type: TokenType = TokenType.access,
        issuer: str | None = "auth",
    ) -> "JWTPayload":
        """
        Factory method to generate a JWT payload with default `iat` and computed `exp`.

        Args:
            sub (int | str): The subject (usually user ID).
            role (str): The user's role. Defaults to "user".
            expire_in (int): Expiration delta in seconds. Defaults to 3600.
            token_type (TokenType): "access" or "refresh". Defaults to "access".
            issuer (str, optional): Token issuer. Defaults to "auth".

        Returns:
            JWTPayload: Fully initialized payload object.
        """
        iat = int(time.time())
        exp = iat + expire_in
        return cls(iss=issuer, typ=token_type, sub=str(sub), iat=iat, exp=exp, role=role)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    access_token_expire_in: int
    refresh_token_expire_in: int


class OAuth2TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
