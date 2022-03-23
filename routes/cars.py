from typing import List

from fastapi import APIRouter, HTTPException, status, Depends, Response
from sqlalchemy import func

from sqlalchemy.orm import Session

from .dependencies import check_db_for_car
from services.car_existence_checker import CarExistenceChecker
from src.database import engine, Base, get_db
from src.schemas import CarCreate, CarInResponse
from src.models import Car, Review

router = APIRouter()

Base.metadata.create_all(bind=engine)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CarCreate)
async def create_car(car: CarCreate, db: Session = Depends(get_db)):
    car_checker = CarExistenceChecker(car_make=car.make, car_model=car.model)
    if not car_checker.car_exists:
        raise HTTPException(status_code=400, detail="There is no such car.")

    check_db_for_car(car, db)

    car_db_model = Car()
    car_db_model.model = car_checker.clean_car_model
    car_db_model.make = car_checker.clean_car_make

    db.add(car_db_model)
    db.commit()

    return CarCreate(
        make=car_checker.clean_car_make,
        model=car_checker.clean_car_model
    )


@router.get("/", response_model=List[CarInResponse])
async def get_all_cars(db: Session = Depends(get_db)):
    return db.query(
        Car.id,
        Car.make,
        Car.model,
        func.round(func.avg(Review.rating), 2).label("avg_rating")
    ).outerjoin(
        Review, Car.id == Review.car_id
    ).group_by(
        Car.id
    ).all()


@router.delete("/{car_id}/")
async def delete_car(car_id: int, db: Session = Depends(get_db)):
    car_db_model = db.query(Car).filter(Car.id == car_id).first()

    if car_db_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No car with given id ({car_id}) in the database."
        )

    db.query(Car).filter(Car.id == car_id).delete()
    db.commit()
    return {"status": status.HTTP_200_OK, "transaction": "Successful"}
