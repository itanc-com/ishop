from app.common.exceptions.app_exceptions import InvalidPayloadException
from app.modules.auth.schemas import JWTPayload, TokenType
from app.utils.jwt_auth.auth_config import ACCESS_TOKEN_EXPIRE, JWT_ISSUER_SERVER, REFRESH_TOKEN_EXPIRE
from app.utils.jwt_auth.jwt_handler import JWThandler


class CreateTokens:
    def __init__(self, user_id: str, user_role: str) -> None:
        self.sub = user_id
        self.role = user_role


    async def execute(self) -> dict | None:
        #* create access-token
        pyaload_access_token : JWTPayload = JWTPayload.create(
            sub=str(self.sub),
            role=self.role,
            token_type=TokenType.access,
            issuer=JWT_ISSUER_SERVER,
            expire_in= ACCESS_TOKEN_EXPIRE,
        )
        
        try:
            access_token = JWThandler.create_token(pyaload_access_token.model_dump())
        except(ValueError, TypeError) as e:
            raise InvalidPayloadException(
                message=f"Failed to create access token, {e}",
                payload=pyaload_access_token.model_dump()
            ) from e
           

        #* create refresh-token
        pyaload_refresh_token : JWTPayload = JWTPayload.create(
            sub=str(self.sub),
            role=self.role,
            token_type=TokenType.refresh,
            issuer=JWT_ISSUER_SERVER,
            expire_in= REFRESH_TOKEN_EXPIRE,
        )
        
        
        try:
           refresh_token = JWThandler.create_token(pyaload_refresh_token.model_dump())
        except(ValueError, TypeError) as e:
            raise InvalidPayloadException(
                message=f"Failed to create refresh token, {e}",
                payload=refresh_token.model_dump()
            ) from e
           

        return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expire_in": ACCESS_TOKEN_EXPIRE,
                "refresh_token_expire_in": REFRESH_TOKEN_EXPIRE
        }
