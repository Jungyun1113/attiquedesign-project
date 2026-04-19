from functools import wraps
from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt as _bcrypt
from jose import jwt, JWTError

from chalicelib.core.config import settings
from chalicelib.core.exceptions import UnauthorizedError, ForbiddenError, handle_app_error
from chalicelib.core.context import set_user


def hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode("utf-8"), _bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return _bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(user_id: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "role": role, "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise UnauthorizedError("유효하지 않은 토큰입니다.")


def _extract_token_from_request(request) -> Optional[str]:
    auth_header = request.headers.get("authorization", "")
    if not auth_header.startswith("Bearer "):
        return None
    return auth_header[len("Bearer "):]


def _get_app_request():
    """Lazy-import app to avoid circular dependency at module load time."""
    import app as _app_module
    return _app_module.app.current_request


def try_extract_user(request) -> Optional[str]:
    """Extract user_id from token if present, without raising on missing token."""
    token = _extract_token_from_request(request)
    if not token:
        return None
    try:
        payload = decode_token(token)
        set_user(payload["sub"], payload.get("role", "USER"))
        return payload["sub"]
    except UnauthorizedError:
        return None


def _is_options_preflight(request) -> bool:
    return request.method == "OPTIONS"


def require_auth(func):
    """Require valid JWT. Sets user context via ContextVar."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = _get_app_request()
        if _is_options_preflight(request):
            return func(*args, **kwargs)
        try:
            token = _extract_token_from_request(request)
            if not token:
                raise UnauthorizedError()
            payload = decode_token(token)
            set_user(payload["sub"], payload.get("role", "USER"))
            return func(*args, **kwargs)
        except UnauthorizedError as e:
            return handle_app_error(e)
    return wrapper


def require_admin(func):
    """Require valid JWT with ADMIN role."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        request = _get_app_request()
        if _is_options_preflight(request):
            return func(*args, **kwargs)
        try:
            token = _extract_token_from_request(request)
            if not token:
                raise UnauthorizedError()
            payload = decode_token(token)
            if payload.get("role") != "ADMIN":
                raise ForbiddenError()
            set_user(payload["sub"], "ADMIN")
            return func(*args, **kwargs)
        except (UnauthorizedError, ForbiddenError) as e:
            return handle_app_error(e)
    return wrapper
