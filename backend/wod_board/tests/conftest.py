import daiquiri
from httpx import AsyncClient
import pytest

from wod_board import config
from wod_board import models
from wod_board import web
from wod_board.models import movement
from wod_board.models import user
from wod_board.models import wod
from wod_board.models import wod_round
from wod_board.utils import user_utils


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
def db_user(db):
    password = "very-strong-password"
    hashed_password = config.PASSWORD_CTXT.hash(password)
    new_user = user.User(
        email="foo@bar.com", hashed_password=hashed_password, username="foo-boy"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    yield new_user


@pytest.fixture()
def token(db_user):
    yield user_utils.create_access_token(db_user)


@pytest.fixture()
def db_wod(db, db_user):
    new_wod = wod.Wod(title="Murph", is_complete=True, author_id=db_user.id)
    db.add(new_wod)
    db.commit()
    db.refresh(new_wod)

    yield new_wod


@pytest.fixture()
def db_round(db, db_wod):
    new_round = wod_round.Round(position=1, wod_id=db_wod.id)
    db.add(new_round)
    db.commit()
    db.refresh(new_round)

    yield new_round


@pytest.fixture()
def db_movement(db):
    new_movement = movement.Movement(name="Devil Press")
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)

    yield new_movement


@pytest.fixture()
def db_goal(db, db_round, db_movement):
    new_goal = movement.MovementGoal(round_id=db_round.id, movement_id=db_movement.id)
    db.add(new_goal)
    db.commit()
    db.refresh(new_goal)

    yield new_goal


@pytest.fixture()
async def client():
    async with AsyncClient(app=web.app, base_url="http://test") as async_client:
        yield async_client
