from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy import func

from sqlalchemy.orm import Session

from src.database import engine, SessionLocal
from src.schemas import CarSchema, ReviewSchema
from src import models


router = APIRouter(tags=["rate"], responses={404: {"description": "Not found"}})

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/rate")
def rate_car(review: ReviewSchema, db: Session = Depends(get_db)):
    # check if such car exists
    car_id = review.car_id
    car_db_model = db.query(models.Car).filter(models.Car.id == car_id).first()
    if car_db_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No such car in our database."
        )

    # create review
    review_model = models.Review()
    review_model.car_id = car_id
    review_model.rating = review.rating

    db.add(review_model)
    db.commit()
    return {"status": status.HTTP_201_CREATED, "transaction": "Successful"}


@router.get("/popular")
def get_cars_by_popularity(db: Session = Depends(get_db)):
    car_reviews = (
        db.query(
            models.Review.car_id, func.count(models.Review.rating).label("rates_number")
        )
        .group_by(models.Review.car_id)
        .subquery()
    )

    object_list = (
        db.query(models.Car, car_reviews.c.rates_number)
        .outerjoin(car_reviews, models.Car.id == car_reviews.c.car_id)
        .all()
    )
    for obj, rates_number in object_list:
        obj.rates_number = rates_number

    return db.query(models.Car).all()
