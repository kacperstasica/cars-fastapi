from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String)
    model = Column(String, unique=True)

    reviews = relationship("Review", back_populates="car")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    car_id = Column(Integer, ForeignKey("cars.id"))

    car = relationship("Car", back_populates="reviews")
