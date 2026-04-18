from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel


class ProductImageResponse(BaseModel):
    id: str
    image_url: str
    display_order: int
    is_primary: bool


class ProductResponse(BaseModel):
    id: str
    sku: str
    name: str
    category: str
    price: Optional[Decimal]
    stock_quantity: int
    status: str
    thumbnail_url: Optional[str]
    images: List[ProductImageResponse] = []
