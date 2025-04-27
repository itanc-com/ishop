from decouple import config
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL: str = str(config("SQLALCHEMY_DATABASE_URL", default="sqlite:///db/db.sqlite3"))

DEBUG: bool = config("DEBUG", default=False, cast=bool)
DOCS: bool = config("DOCS", default=False, cast=bool)

# SECRET_KEY: str = str(config("SECRET_KEY"))
# ALGORITHM: str = str(config("ALGORITHM"))
# ACCESS_TOKEN_EXPIRE_MINUTES: int = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))
