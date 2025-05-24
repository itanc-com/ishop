from app.common.exceptions.app_exceptions import InvalidPayloadException
from app.modules.auth.schemas import JWTPayload
from app.utils.jwt_auth.jwt_handler import JWThandler


class ReadAccessToken:
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token

    async def execute(self) -> JWTPayload:
        """
        Decode the access token and return the payload.

        Returns:
            JWTPayload: The decoded payload of the access token.
        """
        try:
            payload = JWThandler.read_token(self.access_token)
            return JWTPayload.model_validate(payload)
        except Exception as e:
            raise InvalidPayloadException(message=f"Failed to decode access token, {e}", payload=self.access_token)
