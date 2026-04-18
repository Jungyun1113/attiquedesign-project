from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel
from chalicelib.models.reservation import ReservationType, ReservationStatus


class ReservationCreateRequest(BaseModel):
    reservation_type: ReservationType
    expected_date: Optional[datetime] = None
    guest_info: Optional[Any] = None
    dynamic_data: Optional[Any] = None


class ReservationStatusUpdateRequest(BaseModel):
    status: ReservationStatus
