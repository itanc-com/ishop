from fastapi.security import OAuth2PasswordBearer

from app.core.config.constants import AUTH_TOKEN_SWAGGER

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl=AUTH_TOKEN_SWAGGER,
)
