from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func, desc

from sqlalchemy.orm import Session

from src.database import engine, SessionLocal
from src.models import Car, Review
from src.schemas import ReviewSchema
from src import models


router = APIRouter()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/rate/", status_code=status.HTTP_201_CREATED)
def rate_car(review: ReviewSchema, db: Session = Depends(get_db)):
    # check if such car exists
    car_id = review.car_id
    car_db_model = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car_db_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Car not found"
        )

    review_model = models.Review()
    review_model.car_id = car_id
    review_model.rating = review.rating

    db.add(review_model)
    db.commit()
    return review


@router.get("/popular/")
def get_cars_by_popularity(db: Session = Depends(get_db)):
    return db.query(
        Car.id,
        Car.make,
        Car.model,
        func.count(Review.rating).label("rates_number")
    ).outerjoin(
        Review,
        Car.id == Review.car_id
    ).group_by(
        Car.id
    ).order_by(
        desc("rates_number")
    ).all()
