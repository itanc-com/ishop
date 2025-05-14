from app.modules.auth.schemas import JWTPayload, TokenType
from app.utils.jwt_auth.auth_config import ACCESS_TOKEN_EXPIRE, REFRESH_TOKEN_EXPIRE
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
            issuer="auth",
            expire_in= ACCESS_TOKEN_EXPIRE,
        )
        
        access_token = JWThandler.create_token(pyaload_access_token.model_dump())

        #* create refresh-token
        pyaload_refresh_token : JWTPayload = JWTPayload.create(
            sub=str(self.sub),
            role=self.role,
            token_type=TokenType.refresh,
            issuer="auth",
            expire_in= REFRESH_TOKEN_EXPIRE,
        )
        
        refresh_token = JWThandler.create_token(pyaload_refresh_token.model_dump())


        return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expire_in": ACCESS_TOKEN_EXPIRE,
                "refresh_token_expire_in": REFRESH_TOKEN_EXPIRE
        }
