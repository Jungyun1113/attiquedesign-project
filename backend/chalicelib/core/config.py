from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    def __init__(self):
        db_url = os.getenv("DATABASE_URL", "")
        # 만약 환경 변수가 오염되어 있다면(잘못된 에러 메시지가 들어있다면) 정상 주소로 강제 복구
        if db_url.startswith("Failed to add secret") or not db_url.startswith("postgresql"):
            print("WARNING: Corrupted DATABASE_URL detected. Using hardcoded fallback.")
            # SSL 설정을 위해 ?sslmode=require 추가
            db_url = "postgresql+psycopg2://postgres:axHQ2KTOi6oANghBWhLV@attiquedesign-db.cw9iic2c8iu9.us-east-1.rds.amazonaws.com:5432/attiquedesign?sslmode=require"
        
        self.DATABASE_URL: str = db_url
        self.JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-in-production")
        self.JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
        self.REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "30"))

        self.S3_BUCKET: str = os.getenv("S3_BUCKET", "")
        self.AWS_REGION: str = os.getenv("APP_AWS_REGION", os.getenv("AWS_REGION", "ap-northeast-2"))
        self.PRESIGN_EXPIRY_SECONDS: int = int(os.getenv("PRESIGN_EXPIRY_SECONDS", "300"))

        self.PORTONE_API_SECRET: str = os.getenv("PORTONE_API_SECRET", "")
        self.PORTONE_WEBHOOK_SECRET: str = os.getenv("PORTONE_WEBHOOK_SECRET", "")

        self.ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "*")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
