from fastapi import APIRouter, HTTPException, status, Depends

from sqlalchemy.orm import Session

from services.car_existence_checker import CarExistenceChecker
from src.database import engine, SessionLocal
from src.schemas import CarSchema
from src import models


router = APIRouter(
    prefix="/cars",
    tags=["cars"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def create_car(
        car: CarSchema,
        db: Session = Depends(get_db)
):

    car_make = car.make
    car_model = car.model

    car_checker = CarExistenceChecker(car_make=car_make, car_model=car_model)
    if not car_checker.car_exists:
        raise HTTPException(status_code=400, detail="There is no such car.")

    check_db_for_car(car, db)

    car_db_model = models.Car()
    car_db_model.model = car.model
    car_db_model.make = car.make

    db.add(car_db_model)
    db.commit()

    return successful_response(status.HTTP_201_CREATED)


@router.get("/")
async def get_all_cars(db: Session = Depends(get_db)):
    return db.query(models.Car).all()


@router.delete("/{car_id}")
async def delete_car(
        car_id: int,
        db: Session = Depends(get_db)
):
    car_db_model = db.query(
        models.Car
    ).filter(
        models.Car.id == car_id
    ).first()

    if car_db_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such car in the database."
        )

    db.query(models.Car).filter(models.Car.id == car_id).delete()
    db.commit()
    return successful_response(status.HTTP_200_OK)


def check_db_for_car(car, db):
    car = db.query(models.Car).filter(models.Car.model == car.model).first()
    if car is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Car with this model already exists in our database."
        )


def successful_response(status_type: int):
    return {
        'status': status_type,
        'transaction': 'Successful'
    }
