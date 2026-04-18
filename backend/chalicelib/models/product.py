from enum import Enum
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from sqlmodel import Field, Relationship
from chalicelib.models.base import BaseModel


class ProductStatus(str, Enum):
    ACTIVE = "ACTIVE"
    HIDDEN = "HIDDEN"
    SOLDOUT = "SOLDOUT"


class Product(BaseModel, table=True):
    __tablename__ = "products"

    sku: str = Field(unique=True, index=True)
    name: str
    category: str
    price: Optional[Decimal] = Field(default=None)
    stock_quantity: int = Field(default=0)
    status: ProductStatus = Field(default=ProductStatus.ACTIVE)
    thumbnail_url: Optional[str] = Field(default=None)

    images: List["ProductImage"] = Relationship(back_populates="product")


class ProductImage(BaseModel, table=True):
    __tablename__ = "product_images"

    product_id: UUID = Field(foreign_key="products.id", ondelete="CASCADE")
    image_url: str
    display_order: int = Field(default=0)
    is_primary: bool = Field(default=False)

    product: Optional[Product] = Relationship(back_populates="images")
