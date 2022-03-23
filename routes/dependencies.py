from fastapi import HTTPException, status

from src.models import Car


def check_db_for_car(car, db):
    car = db.query(Car).filter(Car.model == car.model).first()
    if car is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car with this model already exists in our database.",
        )
