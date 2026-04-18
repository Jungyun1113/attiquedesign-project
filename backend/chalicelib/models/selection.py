from typing import Optional, List
from uuid import UUID

from sqlmodel import Field, Relationship
from chalicelib.models.base import BaseModel


class Selection(BaseModel, table=True):
    __tablename__ = "selections"

    title: str
    subtitle: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)

    images: List["SelectionImage"] = Relationship(back_populates="selection")
    selection_products: List["SelectionProduct"] = Relationship(back_populates="selection")


class SelectionImage(BaseModel, table=True):
    __tablename__ = "selection_images"

    selection_id: UUID = Field(foreign_key="selections.id", ondelete="CASCADE")
    image_url: str
    display_order: int = Field(default=0)

    selection: Optional[Selection] = Relationship(back_populates="images")


class SelectionProduct(BaseModel, table=True):
    __tablename__ = "selection_products"

    selection_id: UUID = Field(foreign_key="selections.id", ondelete="CASCADE")
    product_id: UUID = Field(foreign_key="products.id", ondelete="RESTRICT")
    display_order: int = Field(default=0)

    selection: Optional[Selection] = Relationship(back_populates="selection_products")
