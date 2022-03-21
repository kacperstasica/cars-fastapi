from typing import Optional

from pydantic import BaseModel, Field


class ReviewSchema(BaseModel):
    rating: int = Field(gt=0, lt=6, description="The rating must be between 1-5")
    car_id: int

    class Config:
        orm_mode = True


class CarSchema(BaseModel):
    make: str
    model: str
    avg_rating: Optional[float] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "make": "Volkswagen",
                "model": "Gold",
            }
        }
