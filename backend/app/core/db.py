# Standard library imports
from typing import Generator

# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

# Local imports
from app.core.config import get_settings
from app.models.base import Base

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)

def get_session() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    if settings.ENV.lower() == "dev":
        Base.metadata.create_all(bind=engine)
