from fastapi.testclient import TestClient
import pytest

from wod_board import models
from wod_board import web


@pytest.fixture()
def db():
    models.create_all()
    try:
        with models.Session() as session:
            yield session
    finally:
        models.drop_all()


@pytest.fixture()
def client():
    yield TestClient(web.app)
