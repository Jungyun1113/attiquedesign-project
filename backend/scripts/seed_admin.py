import sys
import os
from pathlib import Path

# backend 디렉토리를 path에 추가하여 chalicelib 임포트 가능하게 설정
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from dotenv import load_dotenv
load_dotenv(backend_dir / ".env")

from chalicelib.core.db import get_engine, create_db_and_tables
from chalicelib.models.user import User, UserRole, AuthProvider
from chalicelib.core.auth import hash_password
from sqlmodel import Session, select


def seed_admin():
    print("--- Admin Account Seeding Start ---")
    
    # 1. 테이블 생성 확인 (없으면 생성)
    # create_db_and_tables을 호출하기 위해 모델 임포트 필요
    from chalicelib.models import user, product, order, reservation, portfolio, selection, waitlist # noqa
    create_db_and_tables()
    
    engine = get_engine()
    if not engine:
        print("ERROR: Database engine could not be created. Check your DATABASE_URL in .env")
        return

    admin_email = os.getenv("ADMIN_EMAIL", "admin@attique.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin1234!")
    admin_name = "최고관리자"

    with Session(engine) as session:
        # 이미 존재하는지 확인
        statement = select(User).where(User.email == admin_email)
        existing_admin = session.exec(statement).first()
        
        if existing_admin:
            print(f"INFO: Admin account with email '{admin_email}' already exists.")
            # 비밀번호 업데이트 (선택 사항)
            existing_admin.password_hash = hash_password(admin_password)
            session.add(existing_admin)
            session.commit()
            print("INFO: Admin password has been updated.")
        else:
            # 새 관리자 생성
            new_admin = User(
                email=admin_email,
                password_hash=hash_password(admin_password),
                name=admin_name,
                role=UserRole.ADMIN,
                auth_provider=AuthProvider.LOCAL,
                phone="010-0000-0000"
            )
            session.add(new_admin)
            session.commit()
            print(f"SUCCESS: Admin account created: {admin_email}")

    print("--- Seeding Completed ---")


if __name__ == "__main__":
    seed_admin()
