from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from chalicelib.models.product import ProductStatus


class ProductCreateRequest(BaseModel):
    sku: str
    name: str
    category: str
    price: Optional[Decimal] = None
    stock_quantity: int = 0
    status: ProductStatus = ProductStatus.ACTIVE
    thumbnail_url: Optional[str] = None


class ProductUpdateRequest(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    status: Optional[ProductStatus] = None
    thumbnail_url: Optional[str] = None
