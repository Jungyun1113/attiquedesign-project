from datetime import datetime
from enum import Enum
from typing import Optional, Any
from uuid import UUID

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field
from chalicelib.models.base import BaseModel


class ReservationType(str, Enum):
    INTERIOR = "INTERIOR"
    FURNITURE = "FURNITURE"
    TOTAL = "TOTAL"


class ReservationStatus(str, Enum):
    RECEIVED = "RECEIVED"
    IN_PROGRESS = "IN_PROGRESS"
    QUOTED = "QUOTED"
    CONTRACTED = "CONTRACTED"
    NOSHOW = "NOSHOW"


class Reservation(BaseModel, table=True):
    __tablename__ = "reservations"

    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", ondelete="SET NULL")
    guest_info: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
    reservation_type: ReservationType
    status: ReservationStatus = Field(default=ReservationStatus.RECEIVED)
    expected_date: Optional[datetime] = Field(default=None)
    dynamic_data: Optional[Any] = Field(default=None, sa_column=Column(JSONB))
