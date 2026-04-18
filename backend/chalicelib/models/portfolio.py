from typing import Optional, List
from uuid import UUID

from sqlmodel import Field, Relationship
from chalicelib.models.base import BaseModel


class Portfolio(BaseModel, table=True):
    __tablename__ = "portfolios"

    category: str
    title: str
    description: Optional[str] = Field(default=None)
    cover_image_url: Optional[str] = Field(default=None)

    images: List["PortfolioImage"] = Relationship(back_populates="portfolio")


class PortfolioImage(BaseModel, table=True):
    __tablename__ = "portfolio_images"

    portfolio_id: UUID = Field(foreign_key="portfolios.id", ondelete="CASCADE")
    image_url: str
    display_order: int = Field(default=0)

    portfolio: Optional[Portfolio] = Relationship(back_populates="images")
