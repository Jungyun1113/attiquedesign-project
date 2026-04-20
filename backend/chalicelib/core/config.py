from functools import lru_cache
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class Settings:
    def __init__(self):
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "")
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
