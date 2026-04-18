from functools import lru_cache
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from chalicelib.core.config import settings


@lru_cache(maxsize=1)
def get_engine():
    return create_engine(
        settings.DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


def create_db_and_tables():
    SQLModel.metadata.create_all(get_engine())


@contextmanager
def get_session():
    engine = get_engine()
    with Session(engine) as session:
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
