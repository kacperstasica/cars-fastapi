from pydantic import BaseModel, Field


class ReviewSchema(BaseModel):
    rating: int = Field(gt=0, lt=6, description="The rating must be between 1-5")
    car_id: int

    class Config:
        orm_mode = True


class CarBase(BaseModel):
    class Config:
        orm_model = True


class CarCreate(CarBase):
    make: str = "Volkswagen"
    model: str = "Golf"


class CarInResponse(CarBase):
    id: int
    make: str
    model: str
    avg_rating: float | None = None


class CarInResponseByPopularity(CarBase):
    id: int
    make: str
    model: str
    rates_number: int
