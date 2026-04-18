from contextvars import ContextVar
from typing import Optional

_user_id: ContextVar[Optional[str]] = ContextVar("user_id", default=None)
_user_role: ContextVar[Optional[str]] = ContextVar("user_role", default=None)


def set_user(user_id: str, role: str) -> None:
    _user_id.set(user_id)
    _user_role.set(role)


def get_user_id() -> Optional[str]:
    return _user_id.get()


def get_user_role() -> Optional[str]:
    return _user_role.get()


def clear_user() -> None:
    _user_id.set(None)
    _user_role.set(None)
