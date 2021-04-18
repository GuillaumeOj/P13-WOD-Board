import daiquiri
from httpx import AsyncClient
import pytest

from wod_board import config
from wod_board import models
from wod_board import web


@pytest.fixture(autouse=True)
def logs(caplog):
    daiquiri.setup(
        level=config.LOGGING_LEVEL,
    )
    caplog.set_level(config.LOGGING_LEVEL)
    yield caplog


@pytest.fixture()
def db():
    models.create_all()
    try:
        with models.Session() as session:
            yield session
    finally:
        models.drop_all()


@pytest.fixture()
async def client():
    async with AsyncClient(app=web.app, base_url="http://test") as async_client:
        yield async_client
