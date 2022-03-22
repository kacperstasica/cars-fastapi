from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Car(Base):
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String)
    model = Column(String, unique=True)

    __tablename__ = "cars"

    reviews = relationship("Review", back_populates="car")


class Review(Base):
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="cascade"), nullable=True)

    __tablename__ = "reviews"

    car = relationship(
        "Car",
        back_populates="reviews",
    )
