from functools import lru_cache
from contextlib import contextmanager
from sqlmodel import SQLModel, create_engine, Session
from chalicelib.core.config import settings


@lru_cache(maxsize=1)
def get_engine():
    db_url = settings.DATABASE_URL
    if not db_url:
        print("WARNING: DATABASE_URL is not set. Skipping engine creation.")
        return None
        
    try:
        return create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=5,
            max_overflow=10,
        )
    except Exception as e:
        print(f"WARNING: Could not create database engine: {e}")
        return None


def create_db_and_tables():
    engine = get_engine()
    if engine:
        try:
            SQLModel.metadata.create_all(engine)
        except Exception as e:
            print(f"WARNING: Could not create tables: {e}")
    else:
        print("INFO: Skipping table creation because engine is None.")


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
