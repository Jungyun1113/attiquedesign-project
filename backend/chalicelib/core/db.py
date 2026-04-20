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

def seed_admin_if_missing():
    """관리자 계정이 없으면 기본 관리자 정보를 생성합니다."""
    from chalicelib.models.user import User, UserRole, AuthProvider
    from chalicelib.core.auth import hash_password
    from sqlmodel import select, Session
    import os

    engine = get_engine()
    if not engine:
        return

    admin_email = os.getenv("ADMIN_EMAIL", "admin@attique.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin1234!")

    with Session(engine) as session:
        try:
            statement = select(User).where(User.role == UserRole.ADMIN)
            existing_admin = session.exec(statement).first()
            
            if not existing_admin:
                print(f"INFO: Seeding default admin account: {admin_email}")
                new_admin = User(
                    email=admin_email,
                    password_hash=hash_password(admin_password),
                    name="최고관리자",
                    role=UserRole.ADMIN,
                    auth_provider=AuthProvider.LOCAL,
                )
                session.add(new_admin)
                session.commit()
            else:
                print("INFO: Admin account already exists.")
        except Exception as e:
            print(f"WARNING: Could not seed admin account: {e}")
            session.rollback()
