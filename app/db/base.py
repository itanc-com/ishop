from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.common.pydantic.settings import settings

engine = create_engine(
    settings.database_uri,
    connect_args=({"check_same_thread": False} if settings.database_uri.startswith("sqlite") else {}),
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
