from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

from main import app
from src.database import Base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# Base.metadata.create_all(bind=engine)


# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.rollback()
#         db.execute(CLEAR_DB_SQL)
#         db.commit()
#         db.close()


# app.dependency_overrides[get_db] = override_get_db


def test_health(client):
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == status.HTTP_200_OK


# def test_create_car(client, mocked_response):
#     response = client.post(
#         "/cars/",
#         json={"make": "Foo", "model": "Bar"}
#     )
#
#     assert response.status_code == status.HTTP_201_CREATED
#     data = response.json()
#     assert data["model"] == "Bar"
#     assert "id" in data
#     car_id = data["id"]
#
#     response = client.get(f"/{car_id}/")
#     assert response.status_code == status.HTTP_200_OK
#     data = response.json()
#     assert data["model"] == "Bar"
