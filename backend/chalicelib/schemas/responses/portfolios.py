from typing import Optional, List
from pydantic import BaseModel


class PortfolioImageResponse(BaseModel):
    id: str
    image_url: str
    display_order: int


class PortfolioResponse(BaseModel):
    id: str
    category: str
    title: str
    description: Optional[str]
    cover_image_url: Optional[str]
    images: List[PortfolioImageResponse] = []
