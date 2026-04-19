import sys
import os

# backend 디렉토리를 path에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chalicelib.core.db import get_session
from chalicelib.models.user import User, UserRole
from chalicelib.helpers.db import fetch
from chalicelib.core.auth import hash_password

def check_admin():
    email = "admin@example.com"
    with get_session() as session:
        admin = fetch(session, User, email=email)
        if admin:
            print(f"Admin user found: {admin.email} (Role: {admin.role})")
        else:
            print(f"Admin user NOT found. Creating one...")
            from sqlmodel import Session
            from chalicelib.core.db import get_engine
            
            engine = get_engine()
            with Session(engine) as session:
                new_admin = User(
                    email=email,
                    password_hash=hash_password("admin1234"),
                    name="Administrator",
                    role=UserRole.ADMIN
                )
                session.add(new_admin)
                session.commit()
                print("Admin user created successfully with password: admin1234")

if __name__ == "__main__":
    check_admin()
