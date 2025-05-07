from app.common.pydantic.settings import settings

# should connect to aws secret manager or switch on development environment
JWT_SECRET_KEY = settings.jwt_secret_key
JWT_ISSUER_SERVER = settings.jwt_issuer_server
ACCESS_TOKEN_EXPIRE = 60 * 60 * 24  # 24 hours
REFRESH_TOKEN_EXPIRE = 60 * 60 * 24 * 7  # 7 days
JWT_ALGORITHM = "HS256"
