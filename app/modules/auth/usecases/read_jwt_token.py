from app.common.exceptions.app_exceptions import AuthenticationException
from app.modules.auth.schemas import JWTPayload
from app.utils.jwt_auth.jwt_handler import JWThandler


class ReadJwtToken:
    def __init__(self, token: str) -> None:
        self.token = token

    async def execute(self) -> JWTPayload:
        """
        Decode the access token and return the payload.

        Returns:
            JWTPayload: The decoded payload of the access token.
        """
        try:
            payload = JWThandler.read_token(self.token)
            return JWTPayload.model_validate(payload)
        except Exception as e:
            #! avoid user enumeration
            raise AuthenticationException(message=f"Failed to decode  token, {e}")
