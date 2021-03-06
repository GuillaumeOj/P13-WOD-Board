import pytest

from wod_board import exceptions
from wod_board.crud import user_crud
from wod_board.models import user
from wod_board.schemas import user_schemas


def test_create_user(db):
    assert db.query(user.User).count() == 0

    user_schema = user_schemas.UserCreate(
        email="foo@bar.com",
        password="very-strong-password",
        username="foo",
    )
    assert user_crud.create_user(db, user_schema)
    assert db.query(user.User).count() == 1

    with pytest.raises(exceptions.DuplicatedEmail):
        user_crud.create_user(db, user_schema)
    assert db.query(user.User).count() == 1

    user_schema = user_schemas.UserCreate(
        email="bar@foo.com",
        password="very-strong-password",
        username="foo",
    )
    with pytest.raises(exceptions.DuplicatedUsername):
        user_crud.create_user(db, user_schema)
    assert db.query(user.User).count() == 1


def test_get_user_by_id(db, db_user):
    assert db.query(user.User).count() == 1

    wanted_user = user_crud.get_user_by_id(db, db_user.id)
    assert wanted_user.id == db_user.id
    assert db.query(user.User).count() == 1

    with pytest.raises(exceptions.UnknownUser):
        user_crud.get_user_by_id(db, 2)
    assert db.query(user.User).count() == 1


def test_get_user_by_email(db, db_user):
    assert db.query(user.User).count() == 1

    wanted_user = user_crud.get_user_by_email(db, db_user.email)
    assert wanted_user.id == db_user.id
    assert db.query(user.User).count() == 1

    with pytest.raises(exceptions.UnknownUser):
        user_crud.get_user_by_email(db, "bar@foo.com")
    assert db.query(user.User).count() == 1
