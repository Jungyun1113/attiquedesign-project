from enum import Enum
from typing import Optional
from uuid import UUID

from sqlmodel import Field
from chalicelib.models.base import BaseModel


class WaitlistStatus(str, Enum):
    PENDING = "PENDING"
    NOTIFIED = "NOTIFIED"


class Waitlist(BaseModel, table=True):
    __tablename__ = "waitlists"

    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", ondelete="SET NULL")
    contact_method: str
    status: WaitlistStatus = Field(default=WaitlistStatus.PENDING)
