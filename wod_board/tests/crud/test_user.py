import pytest

from wod_board.crud import user as user_crud
from wod_board.schemas import user as user_schemas


default_user = user_schemas.UserCreate(
    email="foo@bar.com",
    password="hashed-password",
    username="foo",
)


def test_create_user(db):
    created_user = user_crud.create_user(db, default_user)

    assert created_user.email == default_user.email
    assert isinstance(created_user.hashed_password, str)
    assert created_user.hashed_password != default_user.password
    assert created_user.username == default_user.username

    assert created_user.id == 1


def test_create_existing_user(db, monkeypatch):
    created_user = user_crud.create_user(db, default_user)
    assert created_user.email == default_user.email

    with pytest.raises(user_crud.DuplicatedEmail):
        user_crud.create_user(db, default_user)

    with monkeypatch.context() as m:
        m.setattr(default_user, "email", "foo2@bar.com")
        with pytest.raises(user_crud.DuplicatedUsername):
            user_crud.create_user(db, default_user)
