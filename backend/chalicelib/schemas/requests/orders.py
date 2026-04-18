from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel


class OrderItemRequest(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: Decimal


class OrderCreateRequest(BaseModel):
    items: List[OrderItemRequest]
    guest_email: Optional[str] = None
    guest_phone: Optional[str] = None
    guest_name: Optional[str] = None
