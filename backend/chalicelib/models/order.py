from enum import Enum
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from sqlmodel import Field, Relationship
from chalicelib.models.base import BaseModel


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class Order(BaseModel, table=True):
    __tablename__ = "orders"

    user_id: Optional[UUID] = Field(default=None, foreign_key="users.id", ondelete="SET NULL")
    guest_email: Optional[str] = Field(default=None)
    guest_phone: Optional[str] = Field(default=None)
    guest_name: Optional[str] = Field(default=None)
    total_amount: Decimal
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    pg_transaction_id: Optional[str] = Field(default=None)

    items: List["OrderItem"] = Relationship(back_populates="order")


class OrderItem(BaseModel, table=True):
    __tablename__ = "order_items"

    order_id: UUID = Field(foreign_key="orders.id", ondelete="CASCADE")
    product_id: UUID = Field(foreign_key="products.id", ondelete="RESTRICT")
    quantity: int
    unit_price: Decimal

    order: Optional[Order] = Relationship(back_populates="items")
