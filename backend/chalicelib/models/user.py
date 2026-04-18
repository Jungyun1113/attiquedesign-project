from enum import Enum
from typing import Optional
from sqlmodel import Field
from chalicelib.models.base import BaseModel


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class AuthProvider(str, Enum):
    LOCAL = "LOCAL"
    KAKAO = "KAKAO"
    NAVER = "NAVER"
    APPLE = "APPLE"


class User(BaseModel, table=True):
    __tablename__ = "users"

    email: str = Field(unique=True, index=True)
    password_hash: Optional[str] = Field(default=None)
    name: str
    phone: Optional[str] = Field(default=None)
    role: UserRole = Field(default=UserRole.USER)
    auth_provider: AuthProvider = Field(default=AuthProvider.LOCAL)
