from unittest.mock import patch

# import factory
import pytest
from fastapi.testclient import TestClient

from main import app

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client

#
# @pytest.fixture()
# def mocked_response():
#     with patch(
#             "services.car_existence_checker.CarExistenceChecker.get_cars_response",
#             return_value=[
#                 {
#                     'Make_ID': 482,
#                     'Make_Name': 'Foo',
#                     'Model_ID': 1951,
#                     'Model_Name': 'Bar'
#                 }
#             ]
#     ):
#         result = CarExistenceChecker("Foo", "Bar")
#         yield result
