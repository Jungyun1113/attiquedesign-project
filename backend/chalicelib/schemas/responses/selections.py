from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel


class SelectionImageResponse(BaseModel):
    id: str
    image_url: str
    display_order: int


class SelectionProductResponse(BaseModel):
    id: str
    product_id: str
    display_order: int
    name: Optional[str] = None
    thumbnail_url: Optional[str] = None
    price: Optional[Decimal] = None
    status: Optional[str] = None


class SelectionResponse(BaseModel):
    id: str
    title: str
    subtitle: Optional[str]
    description: Optional[str]
    images: List[SelectionImageResponse] = []
    products: List[SelectionProductResponse] = []
