from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel


class OrderItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    unit_price: Decimal


class OrderResponse(BaseModel):
    id: str
    user_id: Optional[str]
    guest_email: Optional[str]
    guest_name: Optional[str]
    total_amount: Decimal
    status: str
    pg_transaction_id: Optional[str]
    created_at: str
    items: List[OrderItemResponse] = []
