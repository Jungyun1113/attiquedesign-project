from typing import Optional, Any
from pydantic import BaseModel


class ReservationResponse(BaseModel):
    id: str
    user_id: Optional[str]
    reservation_type: str
    status: str
    expected_date: Optional[str]
    guest_info: Optional[Any]
    dynamic_data: Optional[Any]
    created_at: str
