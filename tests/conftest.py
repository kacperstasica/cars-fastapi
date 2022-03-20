import pytest
from starlette.testclient import TestClient

from main import app
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client
