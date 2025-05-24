from fastapi.security import OAuth2PasswordBearer

oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/auth/token/swagger",
)
