from pydantic import BaseModel


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    phone: str | None
    role: str
    auth_provider: str
