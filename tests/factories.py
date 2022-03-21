import factory

from src.database import SessionLocal
from src.models import Car, Review


class CarFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Car
        sqlalchemy_session = SessionLocal()


# class ReviewFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = Review
#         sqlalchemy_session = SessionLocal
