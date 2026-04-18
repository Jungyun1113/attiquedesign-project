from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar

from sqlalchemy import func
from sqlmodel import select, Session

from chalicelib.models.base import BaseModel as AppBaseModel
from chalicelib.core.exceptions import NotFoundError

T = TypeVar("T", bound=AppBaseModel)

_UNSET = object()


def fetch(
    session: Session,
    model: Type[T],
    raise_not_found: bool = False,
    **filters,
) -> Optional[T]:
    stmt = select(model).where(model.is_deleted == False)
    for key, value in filters.items():
        stmt = stmt.where(getattr(model, key) == value)
    result = session.exec(stmt).first()
    if result is None and raise_not_found:
        raise NotFoundError(f"{model.__name__} not found.")
    return result


def bulk_fetch(
    session: Session,
    model: Type[T],
    filters: Optional[Dict[str, Any]] = None,
    order_by: Optional[Any] = None,
    page: int = 1,
    size: int = 20,
) -> Tuple[List[T], int]:
    base_stmt = select(model).where(model.is_deleted == False)

    if filters:
        for key, value in filters.items():
            if value is not None:
                base_stmt = base_stmt.where(getattr(model, key) == value)

    # COUNT(*) on subquery — no full-table fetch
    count_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = session.exec(count_stmt).one()

    if order_by is not None:
        base_stmt = base_stmt.order_by(order_by)
    else:
        base_stmt = base_stmt.order_by(model.created_at.desc())

    base_stmt = base_stmt.offset((page - 1) * size).limit(size)
    items = list(session.exec(base_stmt).all())

    return items, total


def insert(session: Session, model: Type[T], data: Dict[str, Any]) -> T:
    instance = model(**data)
    session.add(instance)
    session.flush()
    session.refresh(instance)
    return instance


def update(session: Session, instance: T, data: Dict[str, Any]) -> T:
    """Update fields. Pass value=None to explicitly set a field to NULL."""
    for key, value in data.items():
        setattr(instance, key, value)
    instance.updated_at = datetime.now(timezone.utc)
    session.add(instance)
    session.flush()
    session.refresh(instance)
    return instance


def delete(session: Session, instance: T, soft: bool = True) -> None:
    if soft:
        instance.is_deleted = True
        instance.updated_at = datetime.now(timezone.utc)
        session.add(instance)
        session.flush()
    else:
        session.delete(instance)
        session.flush()
