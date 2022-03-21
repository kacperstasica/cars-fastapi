from tests.factories import CarFactory


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_delete_car(client):
    car = CarFactory(model="Golf", make="Volkswagen")
    # to be continued